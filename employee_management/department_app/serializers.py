from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Department
from .models import Employee


class EmployeeSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'date_of_birth', 'salary']


class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializerNested(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'employees']
        extra_kwargs = {'name': {'required': True}, 'id': {'read_only': True}}


class DepartmentSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(EmployeeSerializerNested):
    related_department = DepartmentSerializerNested(many=False, read_only=True)
    related_department_pk = serializers.IntegerField(write_only=True)

    class Meta:
        model = Employee
        fields = EmployeeSerializerNested.Meta.fields + [
            'related_department', 'related_department_pk']

    def get_related_department(self, department_pk):
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
        department_pk = validated_data.pop('related_department_pk')
        department = self.get_related_department(department_pk)

        employee = Employee.objects.create(
            related_department=department,
            **validated_data
        )

        return employee

    def update(self, instance, validated_data):
        department_pk = validated_data.pop('related_department_pk')
        department = self.get_related_department(department_pk)

        instance.related_department = department
        instance.salary = validated_data.get('salary', instance.salary)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance