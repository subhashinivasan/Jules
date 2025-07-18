import unittest
import json
import copy
from app import app, employees

class TestEmployeeAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        global employees
        self.original_employees = copy.deepcopy(employees)

    def tearDown(self):
        global employees
        employees[:] = self.original_employees

    def test_get_employees(self):
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)

    def test_create_employee(self):
        employee_data = {'name': 'Peter Jones', 'position': 'Analyst'}
        response = self.app.post('/employees',
                                 data=json.dumps(employee_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'Peter Jones')
        self.assertEqual(len(employees), 3)

    def test_update_employee(self):
        employee_data = {'name': 'John Doe Updated', 'position': 'Senior Manager'}
        response = self.app.put('/employees/1',
                                data=json.dumps(employee_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'John Doe Updated')
        self.assertEqual(employees[0]['name'], 'John Doe Updated')

    def test_delete_employee(self):
        response = self.app.delete('/employees/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(employees), 1)

if __name__ == '__main__':
    unittest.main()
