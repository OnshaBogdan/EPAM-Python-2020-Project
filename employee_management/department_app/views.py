from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .filters import DepartmentFilter, EmployeeFilter


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

    filterset_class = DepartmentFilter


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
    filterset_class = EmployeeFilter


class DepartmentEmployeesList(generics.ListCreateAPIView):
    """
    ListCreateAPIVIew for Department's Employees.

    list: List all employees of the given department
    create: Create new employee with the given department as related_repartment
    """
    serializer_class = EmployeeSerializerNested
    filterset_class = EmployeeFilter

    def get_queryset(self):
        """
        Returns Employees list with of the given department.
        """
        queryset = Employee.objects.all()
        department_pk = self.kwargs['pk']

        return queryset.filter(related_department__pk=department_pk)

    def create(self, request, *args, **kwargs):
        """
        Create new Employee instance with the given related_department pk.
        """
        request.data['related_department_pk'] = self.kwargs['pk']
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentEmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for Department's Employee.

    retrieve: Retrieve employee with the given department_pk and pk
    update: Update employee data
    partial_update: Patch employee data
    destroy: Delete employee
    """
    serializer_class = EmployeeSerializerNested

    def get_object(self):
        """
        Returns employee instance with the given pk and related_repartment pk.

        :raises Employee.DoesNotExist
        """
        try:
            return Employee.objects.get(
                related_department__pk=self.kwargs['department_pk'],
                pk=self.kwargs['pk']
            )
        except Employee.DoesNotExist:
            raise NotFound(detail='Employee with the given id does not exist.')

    def put(self, request, *args, **kwargs):
        """
        Updates Employee instance with the given pk and related_department pk.
        """
        employee = self.get_object()
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
