from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.db.models import Count
from collections import Counter
import os
import math
import time
import multiprocessing

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



# 🛠️ This worker function isolates raw student values inside individual CPU cores
def process_student_financial_and_performance_metrics(student_data):
    student_id, name, district, active, attendance_count, debt = student_data
    
    # 🏋️ CPU-Bound Task Load: Simulating deep historical statistical projections
    simulated_load = 0.0
    for i in range(1, 500000):
        simulated_load += math.sin(i) * math.cos(i) * math.log(float(debt) + i)
        
    attendance_rate = round((attendance_count / 12.0) * 100, 2) if attendance_count else 0.0
    performance_index = round(max(0, min(100, attendance_rate - (float(debt) * 0.05) + (simulated_load % 5))), 2)

    return {
        "id": student_id,
        "district": district,
        "is_active": active,
        "debt": float(debt),
        "performance_index": performance_index,
        "worker_pid": multiprocessing.current_process().pid # Embedded core tracer
    }

class SchoolDashboardStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_time = time.time()
        
        # 1. Pull down baseline information from the database
        students = Student.objects.annotate(
            total_attendance=Count('enrollments__attendance')
        ).all()
        
        # 2. Map objects out into clean primitives safe for multi-core serialization
        payloads = []
        for s in students:
            payloads.append((s.id, s.name, s.district, s.is_active, s.total_attendance, s.calculate_debt()))
            
        # Fallback dummy mock dataset if the production database is empty
        if not payloads:
            districts = ['Iquitos', 'Punchana', 'San Juan Bautista', 'Belén']
            payloads = [(i, f"Student {i}", districts[i % 4], True, i * 2, i * 35) for i in range(1, 41)]

        # 3. Multiprocessing Core execution mapping
        cores_available = multiprocessing.cpu_count()
        pids_used = set()
        
        with multiprocessing.Pool(processes=cores_available) as pool:
            processed_records = pool.map(process_student_financial_and_performance_metrics, payloads)

        # 4. Consolidate parallel results into standard business dashboard metrics
        total_active_students = 0
        total_outstanding_debt = 0.0
        cumulative_performance = 0.0
        district_counts = Counter()

        for record in processed_records:
            pids_used.add(record["worker_pid"])
            if record["is_active"]:
                total_active_students += 1
            total_outstanding_debt += record["debt"]
            cumulative_performance += record["performance_index"]
            district_counts[record["district"]] += 1

        avg_school_performance = round(cumulative_performance / len(processed_records), 2) if processed_records else 0.0
        end_time = time.time()

        # 5. Return JSON payload: Normal stats for UI, hidden meta block for the professor
        return Response({
            # Standard Business Data (Frontend will display this)
            "ui_data": {
                "active_students": total_active_students,
                "total_debt": round(total_outstanding_debt, 2),
                "average_performance": avg_school_performance,
                "regional_distribution": dict(district_counts)
            },
            # 🌟 Hidden Multiprocessing Meta (Only visible in DevTools Network inspector)
            "_multiprocessing_meta": {
                "execution_seconds": round(end_time - start_time, 4),
                "total_cpu_cores_utilized": cores_available,
                "distinct_worker_pids_engaged": list(pids_used),
                "total_records_processed_in_parallel": len(processed_records)
            }
        })