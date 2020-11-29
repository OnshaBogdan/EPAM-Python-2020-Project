from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class DepartmentEmployeesList(APIView):
    def get(self, request, pk):
        queryset = Employee.objects.filter(related_department__pk=pk)
        serializer = EmployeeSerializerNested(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        request.data['related_department_pk'] = pk
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentEmployeeDetail(APIView):
    def get_object(self, department_pk, pk):
        try:
            return Employee.objects.get(
                related_department__pk=department_pk,
                pk=pk
            )
        except Employee.DoesNotExist:
            raise NotFound(detail='Employee with the given id does not exist.')

    def get(self, request, department_pk, pk):
        employee = self.get_object(department_pk, pk)
        serializer = EmployeeSerializerNested(employee, many=False)
        return Response(serializer.data)

    def put(self, request, department_pk, pk):
        employee = self.get_object(department_pk, pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_pk, pk):
        employee = self.get_object(department_pk, pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
