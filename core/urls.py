from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, PaymentViewSet, TeacherViewSet,
    CourseViewSet, CourseClassViewSet, EnrollmentViewSet, AttendanceViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'classes', CourseClassViewSet, basename='courseclass')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]