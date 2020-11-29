from django.db.utils import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient

from .serializers import *

client = APIClient()


class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(name="Finance")
        Department.objects.create(name="Marketing")

    def test_departments_created(self):
        finance = Department.objects.get(name="Finance")
        marketing = Department.objects.get(name="Marketing")

        self.assertEqual(str(finance), 'Finance Department')
        self.assertEqual(str(marketing), 'Marketing Department')

    def test_departments_create_null(self):
        with self.assertRaises(IntegrityError):
            Department.objects.create()

    def test_departments_create_existing(self):
        with self.assertRaises(IntegrityError):
            Department.objects.create(name="Finance")


class EmployeeTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_employee_created(self):
        employee_1 = Employee.objects.get(name="Shelby Sadler")
        employee_2 = Employee.objects.get(name="Mina Roberts")

        self.assertEqual(str(employee_1),
                         'Shelby Sadler from Finance Department')
        self.assertEqual(str(employee_2),
                         'Mina Roberts from Marketing Department')

    def test_name(self):
        employee = Employee.objects.get(name="Shelby Sadler")
        self.assertEqual(employee.name, 'Shelby Sadler')
        employee.name = 'Aleesha Clark'
        employee.save()
        self.assertEqual(employee.name, 'Aleesha Clark')

    def test_salary(self):
        employee = Employee.objects.get(name="Mina Roberts")
        self.assertEqual(employee.salary, 1300)
        employee.salary = 2000
        employee.save()
        self.assertEqual(employee.salary, 2000)

    def test_date_of_birth(self):
        employee = Employee.objects.get(name="Mina Roberts")
        self.assertEqual(str(employee.date_of_birth), '2000-06-13')
        employee.date_of_birth = '1995-01-01'
        employee.save()
        self.assertEqual(str(employee.date_of_birth), '1995-01-01')

    def test_related_department(self):
        employee = Employee.objects.get(name="Mina Roberts")

        finance_department = Department.objects.get(name='Finance')
        marketing_department = Department.objects.get(name='Marketing')

        self.assertEqual(employee.related_department, marketing_department)
        employee.related_department = finance_department
        employee.save()
        self.assertEqual(employee.related_department, finance_department)


class DepartmentListTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_get_all_departments(self):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        response = client.get('/api/departments/')

        self.assertEqual(serializer.data, response.data)

    def test_create_valid_department(self):
        name = 'Human Resource'
        response = client.post(
            '/api/departments/', data={'name': name}
        )

        department = Department.objects.get(name=name)

        self.assertEqual(department.name, name)
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_department(self):
        response_empty = client.post(
            '/api/departments/', {'name': ''}, format='json'
        )
        response_none = client.post(
            '/api/departments/', {'name': None}, format='json'
        )
        response_missing = client.post(
            '/api/departments/', {}, format='json'
        )

        self.assertEqual(response_empty.status_code, 400)
        self.assertEqual(response_none.status_code, 400)
        self.assertEqual(response_missing.status_code, 400)


class DepartmentDetailTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_get_valid_department(self):
        department = Department.objects.get(name='Finance')
        serializer = DepartmentSerializer(department)

        response = client.get(
            f'/api/departments/{department.pk}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_get_invalid_department(self):
        response = client.get(
            f'/api/departments/999/'
        )

        self.assertEqual(response.status_code, 404)

    def test_put_valid_department(self):
        department = Department.objects.get(name='Finance')
        response = client.put(
            f'/api/departments/{department.pk}/',
            {'name': 'Not a Finance'}
        )
        department_edited = Department.objects.get(pk=department.pk)

        self.assertEqual(department_edited.name, response.data['name'])

    def test_put_invalid_empty_department(self):
        department = Department.objects.get(name='Finance')

        response = client.put(
            f'/api/departments/{department.pk}/',
            {'name': ''}
        )
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_existing_department(self):
        department = Department.objects.get(name='Finance')

        response = client.put(
            f'/api/departments/{department.pk}/',
            {'name': 'Marketing'}
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_valid_department(self):
        department = Department.objects.get(name='Finance')

        response = client.delete(
            f'/api/departments/{department.pk}/'
        )
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(name='Finance')

    def test_delete_invalid_department(self):
        response = client.delete(
            f'/api/departments/999/'
        )
        self.assertEqual(response.status_code, 404)


class EmployeeListTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_get_all_employees(self):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)

        response = client.get('/api/employees/')

        self.assertEqual(serializer.data, response.data)

    def test_create_valid_employee(self):
        department = Department.objects.get(name='Finance')
        data = {
            'name': 'Tarun Nolan',
            'date_of_birth': '1995-11-27',
            'salary': 2000,
            'related_department_pk': department.pk
        }
        response = client.post(
            '/api/employees/', data=data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['related_department']['name'],
            department.name
        )

    def test_create_invalid_employee(self):
        department = Department.objects.get(name='Finance')
        data = {
            'name': 'Tarun Nolan',
            'date_of_birth': '1995-11-27',
            'salary': 2000,
            'related_department_pk': department.pk
        }

        response_1 = client.post(
            '/api/employees/', data=dict(data, related_department_pk='999')
        )
        response_2 = client.post(
            '/api/employees/', data=dict(data, related_department_pk='')
        )
        response_3 = client.post(
            '/api/employees/', data=dict(data, name='')
        )
        response_4 = client.post(
            '/api/employees/', data=dict(data, date_of_birth='')
        )
        response_5 = client.post(
            '/api/employees/', data=dict(data, salary='')
        )

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_4.status_code, 400)
        self.assertEqual(response_5.status_code, 400)


class EmployeeDetailTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_get_valid_employee(self):
        employee = Employee.objects.get(name='Shelby Sadler')
        serializer = EmployeeSerializer(employee)

        response = client.get(
            f'/api/employees/{employee.pk}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_get_invalid_employee(self):
        response = client.get(
            f'/api/employees/999/'
        )

        self.assertEqual(response.status_code, 404)

    def test_put_valid_employee(self):
        employee = Employee.objects.get(name='Shelby Sadler')
        department = Department.objects.get(name='Finance')
        response = client.put(
            f'/api/employees/{employee.pk}/',
            {
                'name': 'Shelby Sadler',
                'salary': 2100,
                'date_of_birth': "1995-11-27",
                'related_department_pk': department.pk
            }
        )
        employee_edited = Employee.objects.get(pk=employee.pk)

        self.assertEqual(employee_edited.name, response.data['name'])
        self.assertEqual(employee_edited.salary, response.data['salary'])

    def test_put_invalid_employee(self):
        employee = Employee.objects.get(name='Shelby Sadler')
        department = Department.objects.get(name='Finance')
        data = {
            'name': 'Shelby Sadler',
            'salary': 2100,
            'date_of_birth': "1995-11-27",
            'related_department_pk': department.pk
        }

        response_1 = client.put(
            f'/api/employees/{employee.pk}/',
            dict(data, name='')
        )
        response_2 = client.put(
            f'/api/employees/{employee.pk}/',
            dict(data, related_department_pk=999)
        )
        response_3 = client.put(
            f'/api/employees/{employee.pk}/',
            dict(data, date_of_birth='')
        )
        response_4 = client.put(
            f'/api/employees/{employee.pk}/',
            dict(data, date_of_birth='2000/0000/0000')
        )

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_4.status_code, 400)

    def test_delete_valid_employee(self):
        employee = Employee.objects.get(name='Shelby Sadler')

        response = client.delete(
            f'/api/employees/{employee.pk}/'
        )
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(name='Shelby Sadler')

    def test_delete_invalid_employee(self):
        response = client.delete(
            f'/api/employees/999/'
        )
        self.assertEqual(response.status_code, 404)


class DepartmentEmployeesListTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_get_department_employees_list(self):
        department = Department.objects.get(name='Finance')

        response = client.get(
            f'/api/departments/{department.pk}/employees/'
        )
        employees = Employee.objects.filter(
            related_department__pk=department.pk
        )
        serializer = EmployeeSerializerNested(employees, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_create_valid_department_employee(self):
        department = Department.objects.get(name='Finance')
        emp_data = {
            'name': 'Cherise Whittle',
            'salary': 1500,
            'date_of_birth': '2000-01-01',
            'related_department_pk': department.pk
        }
        response = client.post(
            f'/api/departments/{department.pk}/employees/',
            data=emp_data,
            format='json'
        )

        employee = Employee.objects.get(name=emp_data['name'])
        serializer = EmployeeSerializer(employee)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_create_invalid_department_employee(self):
        department = Department.objects.get(name='Finance')
        emp_data = {
            'name': 'Cherise Whittle',
            'salary': 1500,
            'date_of_birth': '2000-01-01',
        }
        response_1 = client.post(
            f'/api/departments/{department.pk}/employees/',
            data=dict(emp_data, name=''),
            format='json'
        )

        response_2 = client.post(
            f'/api/departments/{department.pk}/employees/',
            data=dict(emp_data, salary='string'),
            format='json'
        )
        response_3 = client.post(
            f'/api/departments/{department.pk}/employees/',
            data=dict(emp_data, date_of_birth='20000909'),
            format='json'
        )

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)


class DepartmentEmployeeDetailTestCase(TestCase):
    def setUp(self):
        finance_department = Department.objects.create(name="Finance")
        marketing_department = Department.objects.create(name="Marketing")

        Employee.objects.create(
            name="Shelby Sadler",
            salary=2000,
            date_of_birth='1990-01-20',
            related_department=finance_department
        )
        Employee.objects.create(
            name="Mina Roberts",
            salary=1300,
            date_of_birth='2000-06-13',
            related_department=marketing_department
        )

    def test_get_valid_department_employee(self):
        department = Department.objects.get(name='Finance')
        employee = Employee.objects.get(related_department__pk=department.pk)

        self.assertEqual(department.pk, employee.related_department.pk)

        response = client.get(
            f'/api/departments/{department.pk}/employees/{employee.pk}/'
        )
        serializer = EmployeeSerializerNested(employee, many=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_department_employee(self):
        department = Department.objects.get(name='Finance')

        response = client.get(
            f'/api/departments/{department.pk}/employees/999/'
        )

        self.assertEqual(response.status_code, 404)

    def test_put_valid_department_employee(self):
        department = Department.objects.get(name='Finance')
        employee = Employee.objects.get(name='Shelby Sadler')
        response = client.put(
            f'/api/departments/{department.pk}/employees/{employee.pk}/',
            {
                'name': employee.name,
                'salary': employee.salary + 100,
                'date_of_birth': employee.date_of_birth,
                'related_department_pk': employee.related_department.pk,
            }
        )
        employee_edited = Employee.objects.get(name='Shelby Sadler')
        serializer = EmployeeSerializer(employee_edited, many=False)

        self.assertEqual(serializer.data, response.data)

    def test_put_invalid_department_employee(self):
        department = Department.objects.get(name='Finance')
        employee = Employee.objects.get(name='Shelby Sadler')

        data = {
            'name': employee.name,
            'salary': employee.salary + 100,
            'date_of_birth': employee.date_of_birth,
            'related_department_pk': employee.related_department.pk,
        }
        response_1 = client.put(
            f'/api/departments/{department.pk}/employees/{employee.pk}/',
            data=dict(data, name='')
        )
        response_2 = client.put(
            f'/api/departments/{department.pk}/employees/{employee.pk}/',
            data=dict(data, salary='string')
        )
        response_3 = client.put(
            f'/api/departments/{department.pk}/employees/{employee.pk}/',
            data=dict(data, related_department_pk=999)
        )
        response_4 = client.put(
            f'/api/departments/{department.pk}/employees/{employee.pk}/',
            data=dict(data, date_of_birth='invalid')
        )
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_4.status_code, 400)

    def test_delete_valid_department_employee(self):
        employee = Employee.objects.get(name='Shelby Sadler')
        department = Department.objects.get(name='Finance')

        response = client.delete(
            f'/api/departments/{department.pk}/employees/{employee.pk}/'
        )
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(name='Shelby Sadler')


    def test_delete_invalid_employee(self):
        department = Department.objects.get(name='Finance')
        response = client.delete(
            f'/api/departments/{department.pk}/employees/999/'
        )
        self.assertEqual(response.status_code, 404)
