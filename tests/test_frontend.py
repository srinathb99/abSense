from selenium import webdriver
import unittest
from main import app
import time as tm


class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_caution(self):
        tester = app.test_client(self)
        response = tester.get('/caution', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_apply_leave(self):
        tester = app.test_client(self)
        response = tester.get('/apply_leave', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_view_leave(self):
        tester = app.test_client(self)
        response = tester.get('/view_leave', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_student_dashboard(self):
        tester = app.test_client(self)
        response = tester.get('/student_dashboard', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_student_login(self):
        tester = app.test_client(self)
        response = tester.get('/student_login', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_faculty_login(self):
        tester = app.test_client(self)
        response = tester.get('/faculty_login', content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.get('/student_dashboard', content_type='html/text')
        self.assertEqual(response.status_code,200)