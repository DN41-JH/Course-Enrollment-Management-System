"""test_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from CourseManagement import views

router = routers.SimpleRouter()
router.register(r"", viewset=views.DepartmentsViewSet, basename='departments')
router.register(r"", viewset=views.CoursesViewSet, basename='courses')
router.register(r"", viewset=views.StudentsViewSet, basename='students')
router.register(r"", viewset=views.InstructorsViewSet, basename='instructors')
router.register(r"", viewset=views.RegistrationViewSet, basename='registration')
router.register(r"", viewset=views.LoginViewSet, basename='login')
router.register(r"instructor", viewset=views.InstructorViewSet, basename='instructor')
router.register(r"student", viewset=views.StudentViewSet, basename='student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
