import unittest
import os
import sqlite3
import app as app_module
from app import app


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.test_db = os.path.join(app_module.BASE_DIR, 'test_database.db')
        self.original_db = app_module.DATABASE
        app_module.DATABASE = self.test_db
        app_module.init_db()

    def tearDown(self):
        app_module.DATABASE = self.original_db
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def query(self, sql, params=()):
        conn = sqlite3.connect(self.test_db)
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return rows

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<ul', response.data)

    def test_index_newest_first(self):
        self.app.post('/add', data={'title': 'first'})
        self.app.post('/add', data={'title': 'second'})
        html = self.app.get('/').get_data(as_text=True)
        self.assertLess(html.index('second'), html.index('first'))

    def test_add_success(self):
        response = self.app.post('/add', data={'title': '공부하기'}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        rows = self.query("SELECT title FROM todos WHERE title='공부하기'")
        self.assertEqual(rows, [('공부하기',)])

    def test_add_empty(self):
        response = self.app.post('/add', data={'title': ''}, follow_redirects=False)
        self.assertEqual(response.status_code, 400)

    def test_add_whitespace(self):
        response = self.app.post('/add', data={'title': '   '}, follow_redirects=False)
        self.assertEqual(response.status_code, 400)

    def test_add_long_title(self):
        long_title = "A" * 10000
        response = self.app.post('/add', data={'title': long_title}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(long_title.encode(), response.data)
        self.assertEqual(len(self.query("SELECT * FROM todos")), 1)

    def test_toggle_success(self):
        self.app.post('/add', data={'title': '테스트할 일'})

        response = self.app.post('/toggle/1', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.query("SELECT is_completed FROM todos WHERE id=1"), [(1,)])

        # 한 번 더 토글하면 원래 상태로 돌아옴
        self.app.post('/toggle/1')
        self.assertEqual(self.query("SELECT is_completed FROM todos WHERE id=1"), [(0,)])

    def test_toggle_not_found(self):
        response = self.app.post('/toggle/999', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    def test_toggle_invalid_type(self):
        response = self.app.post('/toggle/abc', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    def test_delete_success(self):
        self.app.post('/add', data={'title': '삭제할 일'})

        response = self.app.post('/delete/1', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.query("SELECT * FROM todos WHERE id=1"), [])
        self.assertNotIn('삭제할 일', self.app.get('/').get_data(as_text=True))

    def test_delete_not_found(self):
        response = self.app.post('/delete/999', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    def test_delete_invalid_type(self):
        response = self.app.post('/delete/abc', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    def test_non_existent_route(self):
        response = self.app.get('/non-existent-route')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
