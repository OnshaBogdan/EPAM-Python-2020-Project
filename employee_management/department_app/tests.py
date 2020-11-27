from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Department
from .models import Employee


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
