from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import Student, Payment, Teacher, Course, CourseClass, Enrollment, Attendance
from .filters import (
    StudentFilter, PaymentFilter, TeacherFilter, 
    CourseFilter, CourseClassFilter, EnrollmentFilter, AttendanceFilter
)
from .serializers import (
    StudentSerializer, PaymentSerializer, TeacherSerializer,
    CourseSerializer, CourseClassSerializer, EnrollmentSerializer, AttendanceSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ['name', 'address', 'parent_1_name', 'parent_2_name']
    ordering_fields = ['name', 'enrollment_date']
    permission_classes = [IsAuthenticatedOrReadOnly]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'amount']
    permission_classes = [IsAuthenticatedOrReadOnly]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('name')
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TeacherFilter
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('name')
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CourseFilter
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]

class CourseClassViewSet(viewsets.ModelViewSet):
    queryset = CourseClass.objects.all()
    serializer_class = CourseClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseClassFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EnrollmentFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-date')
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AttendanceFilter
    ordering_fields = ['date']
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthCheckView(APIView):
    # This automatically rejects requests with a 401 Unauthorized if the JWT is invalid or missing
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        return Response({
            "authenticated": True,
            "username": request.user.username,
            "email": request.user.email
        })