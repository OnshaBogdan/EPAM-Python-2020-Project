from django.db import models
from django.db.models import Avg


class Department(models.Model):
    """
    Stores a single Department entity, related to :model:`department_app.Employee`
    """
    name = models.CharField(max_length=30, null=False, default=None, unique=True)

    @property
    def average_salary(self):
        return self.employees.all().aggregate(Avg('salary'))['salary__avg'] or 0

    def __str__(self):
        return f'{self.name} Department'


class Employee(models.Model):
    """
    Stores a single Employee entity, related to :model:`department_app.Employee`
    """
    name = models.CharField(max_length=30, null=False)
    related_department = models.ForeignKey(
        Department,
        null=False,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    date_of_birth = models.DateField(null=False)
    salary = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f'{self.name} from {self.related_department}'
