import django_filters
from .models import Student, Payment, Teacher, Course, CourseClass, Enrollment, Attendance

class StudentFilter(django_filters.FilterSet):
    # Allows filtering by range (e.g., ?enrollment_date_gte=2026-01-01)
    enrollment_date_gte = django_filters.DateFilter(field_name="enrollment_date", lookup_expr='gte')
    enrollment_date_lte = django_filters.DateFilter(field_name="enrollment_date", lookup_expr='lte')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['district', 'is_active', 'name']

class PaymentFilter(django_filters.FilterSet):
    payment_date_gte = django_filters.DateFilter(field_name="payment_date", lookup_expr='gte')
    payment_date_lte = django_filters.DateFilter(field_name="payment_date", lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['student', 'payment_date_gte', 'payment_date_lte']

class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['is_active', 'name']

class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name']

class CourseClassFilter(django_filters.FilterSet):
    class Meta:
        model = CourseClass
        fields = ['course', 'teacher']

class EnrollmentFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = ['course_class', 'student']

class AttendanceFilter(django_filters.FilterSet):
    date = django_filters.DateFilter()

    class Meta:
        model = Attendance
        fields = ['enrollment__course_class', 'enrollment__student', 'date', 'present']