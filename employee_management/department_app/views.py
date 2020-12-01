from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class DepartmentViewSet(ModelViewSet):
    """
    Department ViewSet.

    list: List all departments
    retrieve: Retrieve department with the given id
    update: Update department data
    create: Create new department
    partial_update: Patch department data
    destroy: Delete department
    """
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class EmployeeViewSet(ModelViewSet):
    """
    Employee ViewSet.

    list: List all employees
    retrieve: Retrieve employee with the given id
    update: Update employee data
    create: Create new employee
    partial_update: Patch employee data
    destroy: Delete employee
    """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class DepartmentEmployeesList(APIView):
    """
    Department's employees APIView.
    """

    def get(self, request, pk):
        """
        Get list of department's employees with the given department pk.
        """
        queryset = Employee.objects.filter(related_department__pk=pk)
        serializer = EmployeeSerializerNested(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        Create new Employee instance with the given related_department pk.
        """
        request.data['related_department_pk'] = pk
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentEmployeeDetail(APIView):
    """
    Department's Employee APIView.
    """

    def get_object(self, department_pk, pk):
        """
        Returns employee instance with the given pk and related_repartment pk.

        :raises Employee.DoesNotExist
        """
        try:
            return Employee.objects.get(
                related_department__pk=department_pk,
                pk=pk
            )
        except Employee.DoesNotExist:
            raise NotFound(detail='Employee with the given id does not exist.')

    def get(self, request, department_pk, pk):
        """
        Retrieves a single Employee instance with the given pk and related_department pk.
        """
        employee = self.get_object(department_pk, pk)
        serializer = EmployeeSerializerNested(employee, many=False)
        return Response(serializer.data)

    def put(self, request, department_pk, pk):
        """
        Updates Employee instance with the given pk and related_department pk.
        """
        employee = self.get_object(department_pk, pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_pk, pk):
        """
        Destroys Employee instance with the given pk and related_department pk.
        """
        employee = self.get_object(department_pk, pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
