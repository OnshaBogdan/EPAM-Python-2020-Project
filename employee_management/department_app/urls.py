from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = [
    path('', views.DepartmentsView.as_view(), name='departments'),
    path('departments/<int:pk>/', views.DepartmentView.as_view(), name='department'),
    path('employees/', views.EmployeesView.as_view(), name='employees'),
    path('employees/<int:pk>/', views.EmployeeView.as_view(), name='employee'),


    path('api/', include(router.urls)),
    path('api/departments/<int:pk>/employees/', views.DepartmentEmployeesList.as_view(),
         name='department-employee-list'),
    path('api/departments/<int:department_pk>/employees/<int:pk>/',
         views.DepartmentEmployeeDetail.as_view(),
         name='department-employee-detail'),
]
