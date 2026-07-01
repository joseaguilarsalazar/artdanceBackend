from rest_framework import serializers
from .models import Student, Payment, Teacher, Course, CourseClass, Enrollment, Attendance

class StudentSerializer(serializers.ModelSerializer):
    # Expose the calculated debt dynamically as a read-only field
    debt = serializers.ReadOnlyField(source='calculate_debt')

    class Meta:
        model = Student
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseClassSerializer(serializers.ModelSerializer):
    # String representations for readable nested data
    course_name = serializers.ReadOnlyField(source='course.name')
    teacher_name = serializers.ReadOnlyField(source='teacher.name')

    class Meta:
        model = CourseClass
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        # Enforce the unique_together constraint gracefully via API validation
        if Enrollment.objects.filter(course_class=data['course_class'], student=data['student']).exists():
            raise serializers.ValidationError("This student is already enrolled in this specific class.")
        return data

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'