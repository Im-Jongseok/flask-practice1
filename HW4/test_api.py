import os
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch


class TodoApiTest(unittest.TestCase):
    def setUp(self):
        # SQLAlchemy 초기화 전부터 메모리 DB를 사용해 기존 파일 DB를 보호한다.
        with patch.dict(os.environ, {"TODO_DATABASE_URI": "sqlite:///:memory:"}):
            module = runpy.run_path(str(Path(__file__).with_name("app.py")))

        self.app = module["app"]
        self.db = module["db"]
        self.app.config["TESTING"] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.addCleanup(self.ctx.pop)
        self.addCleanup(self.db.engine.dispose)
        self.addCleanup(self.db.session.remove)
        self.assertEqual(self.db.engine.url.database, ":memory:")
        self.client = self.app.test_client()

    def create_todo(self, text="우유 사기", **fields):
        response = self.client.post("/api/todos/", json={"text": text, **fields})
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def test_list_without_filter_returns_all(self):
        done = self.create_todo(done=True)
        pending = self.create_todo("책 반납")

        response = self.client.get("/api/todos/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item["id"] for item in response.get_json()},
            {done["id"], pending["id"]},
        )

    def test_post_returns_note_and_location(self):
        response = self.client.post(
            "/api/todos/", json={"text": "우유 사기", "note": "2리터짜리로"}
        )
        item = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            item,
            {
                "id": item["id"],
                "text": "우유 사기",
                "done": False,
                "note": "2리터짜리로",
            },
        )
        self.assertEqual(response.headers["Location"], f"/api/todos/{item['id']}")

    def test_post_defaults_note_and_done(self):
        item = self.create_todo()

        self.assertEqual(item["note"], "")
        self.assertFalse(item["done"])

    def test_get_returns_all_fields(self):
        item = self.create_todo(note="2리터짜리로", done=True)

        response = self.client.get(f"/api/todos/{item['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), item)

    def test_patch_only_changes_done(self):
        item = self.create_todo(note="2리터짜리로")

        response = self.client.patch(f"/api/todos/{item['id']}", json={"done": True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {**item, "done": True})

    def test_patch_updates_note_without_changing_other_fields(self):
        item = self.create_todo(note="2리터짜리로", done=True)
        path = f"/api/todos/{item['id']}"

        response = self.client.patch(path, json={"note": "1리터로 변경"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {**item, "note": "1리터로 변경"})
        self.assertEqual(
            self.client.patch(path, json={"note": ""}).get_json()["note"], ""
        )

    def test_filter_by_done(self):
        done = self.create_todo(done=True)
        pending = self.create_todo("책 반납", done=False)

        for value, expected in [("true", done), ("false", pending), ("TRUE", done)]:
            with self.subTest(done=value):
                response = self.client.get(f"/api/todos/?done={value}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), [expected])

    def test_put_replaces_fields_and_resets_omitted_values(self):
        item = self.create_todo(note="기존 설명", done=True)
        path = f"/api/todos/{item['id']}"

        response = self.client.put(
            path, json={"text": "책 반납", "note": "도서관", "done": True}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"id": item["id"], "text": "책 반납", "note": "도서관", "done": True},
        )
        response = self.client.put(path, json={"text": "다시 수정"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["note"], "")
        self.assertFalse(response.get_json()["done"])

    def test_delete_returns_empty_204_then_404(self):
        item = self.create_todo()
        path = f"/api/todos/{item['id']}"

        response = self.client.delete(path)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        self.assertEqual(self.client.get(path).status_code, 404)

    def test_missing_id_returns_404_json(self):
        for method in ["GET", "PUT", "PATCH", "DELETE"]:
            with self.subTest(method=method):
                response = self.client.open(
                    "/api/todos/999", method=method, json={"text": "없는 항목"}
                )
                self.assertEqual(response.status_code, 404)
                self.assertEqual(
                    response.get_json(), {"message": "999 번 할 일이 없습니다"}
                )

    def test_post_missing_text_returns_400(self):
        response = self.client.post("/api/todos/", json={"note": "설명만"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get("/api/todos/").get_json(), [])

    def test_docs_describe_note_filter_and_six_operations(self):
        self.assertEqual(self.client.get("/api/docs").status_code, 200)
        response = self.client.get("/api/swagger.json")
        self.assertEqual(response.status_code, 200)
        schema = response.get_json()

        methods = {"get", "post", "put", "patch", "delete"}
        self.assertEqual(set(schema["paths"]["/todos/"]) & methods, {"get", "post"})
        self.assertEqual(
            set(schema["paths"]["/todos/{id}"]) & methods,
            {"get", "put", "patch", "delete"},
        )
        for model in ["Todo", "TodoInput"]:
            self.assertIn("note", schema["definitions"][model]["properties"])
        self.assertTrue(
            any(
                parameter["name"] == "done" and parameter["in"] == "query"
                for parameter in schema["paths"]["/todos/"]["get"]["parameters"]
            )
        )

    def test_web_routes_share_api_data(self):
        item = self.create_todo()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("우유 사기", response.get_data(as_text=True))
        with self.client.get("/static/style.css") as response:
            self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(f"/toggle/{item['id']}").status_code, 302)
        self.assertTrue(self.client.get(f"/api/todos/{item['id']}").get_json()["done"])
        self.assertEqual(self.client.get(f"/delete/{item['id']}").status_code, 302)
        self.assertEqual(self.client.get(f"/api/todos/{item['id']}").status_code, 404)


if __name__ == "__main__":
    unittest.main()
