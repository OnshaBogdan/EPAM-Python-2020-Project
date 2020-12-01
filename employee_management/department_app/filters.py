from django_filters import rest_framework as filters


class EmployeeFilter(filters.FilterSet):
    salary = filters.NumberFilter(field_name="salary", lookup_expr='iexact')
    salary__gt = filters.NumberFilter(field_name="salary", lookup_expr='gt')
    salary__gte = filters.NumberFilter(field_name="salary", lookup_expr='gte')
    salary__lt = filters.NumberFilter(field_name="salary", lookup_expr='lt')
    salary__lte = filters.NumberFilter(field_name="salary", lookup_expr='lte')

    date_of_birth = filters.DateFilter(field_name="date_of_birth")
    date_of_birth__gte = filters.DateFilter(field_name="date_of_birth", lookup_expr='gte')
    date_of_birth__gt = filters.DateFilter(field_name="date_of_birth", lookup_expr='gt')
    date_of_birth__lte = filters.DateFilter(field_name="date_of_birth", lookup_expr='lte')
    date_of_birth__lt = filters.DateFilter(field_name="date_of_birth", lookup_expr='lt')

    name = filters.CharFilter(field_name="name", lookup_expr='iexact')
    name__contains = filters.CharFilter(field_name="name", lookup_expr='icontains')


class DepartmentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='iexact')
    name__contains = filters.CharFilter(field_name="name", lookup_expr='icontains')
