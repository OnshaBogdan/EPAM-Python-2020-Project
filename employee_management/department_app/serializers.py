from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Department
from .models import Employee


class EmployeeSerializerNested(serializers.ModelSerializer):
    """
    Employee model serializer for usage as nested object.
    """

    class Meta:
        model = Employee
        fields = ['id', 'name', 'date_of_birth', 'salary']


class DepartmentSerializerNested(serializers.ModelSerializer):
    """
    Department model serializer for usage as nested object.
    """
    average_salary = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'average_salary']


class DepartmentSerializer(DepartmentSerializerNested):
    """
    Department model serializer with nested employees data.
    """
    employees = EmployeeSerializerNested(many=True, read_only=True)

    class Meta:
        model = Department
        fields = DepartmentSerializerNested.Meta.fields + ['employees']
        extra_kwargs = {'name': {'required': True}, 'id': {'read_only': True}}


class EmployeeSerializer(EmployeeSerializerNested):
    """
    Employee model serializer with nested related department data.
    """
    related_department = DepartmentSerializerNested(many=False, read_only=True)
    related_department_pk = serializers.IntegerField(write_only=True)

    class Meta:
        model = Employee
        fields = EmployeeSerializerNested.Meta.fields + [
            'related_department', 'related_department_pk']

    def get_related_department(self, department_pk):
        """
        Returns department with the given pk.

        :raises ValidationError
        """
        try:
            return Department.objects.get(pk=department_pk)
        except Department.DoesNotExist:
            raise ValidationError(
                detail={
                    'detail': 'Department with the given id does not exist'
                },
                code=400
            )

    def create(self, validated_data):
        """
        Creates Employee instance with the given validated data.
        """
        department_pk = validated_data.pop('related_department_pk')
        department = self.get_related_department(department_pk)

        employee = Employee.objects.create(
            related_department=department,
            **validated_data
        )

        return employee

    def update(self, instance, validated_data):
        """
        Updates employee instance with the given validated data.
        """
        department_pk = validated_data.pop('related_department_pk')
        department = self.get_related_department(department_pk)

        instance.related_department = department
        instance.salary = validated_data.get('salary', instance.salary)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance
