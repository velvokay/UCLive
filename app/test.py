from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
	#checks for proper flask setup
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	#ensures that login page loads properly
	def test_login_page_loads(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertTrue(b'Login' in response.data)
	
	#ensures that login behaves correctly given proper credentials
	def test_correct_login(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login', 
			data=dict(username="admin", password="admin"), 
			follow_redirects = True
		)
		self.assertIn(b'Successfully logged in.' ,response.data)
		
	#ensures that login behaves correctly given improper credentials
	def test_icorrect_login(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login', 
			data=dict(username="wrong", password="admin"), 
			follow_redirects = True
		)
		self.assertIn(b'Invalid credentials. Please try again.' ,response.data)
	
	#ensures that logout behaves correctly
	def test_logout(self):
		tester = app.test_client(self)
		tester.post(
			'/login', 
			data=dict(username="admin", password="admin"), 
			follow_redirects = True
		)
		response = tester.get('/logout', follow_redirects = True)
		self.assertIn(b'Successfully logged out.' ,response.data)
		
	#ensures that dashboard requires login
	def test_dashboard_route_requires_login(self):
		tester = app.test_client(self)
		response = tester.get('/dashBoard', follow_redirects = True)
		self.assertTrue(b'Please login first.' in response.data)
	
if __name__ == '__main__':
	unittest.main()