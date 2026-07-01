from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, PaymentViewSet, TeacherViewSet,
    CourseViewSet, CourseClassViewSet, EnrollmentViewSet, AttendanceViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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
    # The login view: accepts 'username' and 'password', returns access/refresh keys
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # The token cycle view: accepts a valid refresh token, returns a fresh access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]