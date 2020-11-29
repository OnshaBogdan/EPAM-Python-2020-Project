from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/departments/<int:pk>/employees/', views.DepartmentEmployeesList.as_view(),
         name='department-employee-list'),
    path('api/departments/<int:department_pk>/employees/<int:pk>/',
         views.DepartmentEmployeeDetail.as_view(),
         name='department-employee-detail'),
]
