from django.db import models
from django.db.models import Sum
from django.utils import timezone
import datetime
from decimal import Decimal

class DistrictChoices(models.TextChoices):
    IQUITOS = 'Iquitos', 'Iquitos'
    PUNCHANA = 'Punchana', 'Punchana'
    SAN_JUAN = 'San Juan Bautista', 'San Juan Bautista'
    BELEN = 'Belén', 'Belén'

class DayChoices(models.TextChoices):
    MONDAY = 'MON', 'Monday'
    TUESDAY = 'TUE', 'Tuesday'
    WEDNESDAY = 'WED', 'Wednesday'
    THURSDAY = 'THU', 'Thursday'
    FRIDAY = 'FRI', 'Friday'
    SATURDAY = 'SAT', 'Saturday'
    SUNDAY = 'SUN', 'Sunday'

class Student(models.Model):
    name = models.CharField(max_length=100)
    # Changed from auto_now_add so you can backdate enrollments
    enrollment_date = models.DateField(default=timezone.now)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    district = models.CharField(max_length=50, choices=DistrictChoices.choices, default=DistrictChoices.IQUITOS)
    
    # Parent details grouped logically
    parent_1_name = models.CharField(max_length=100, blank=True, null=True)
    parent_1_number = models.CharField(max_length=20, blank=True, null=True)
    parent_2_name = models.CharField(max_length=100, blank=True, null=True)
    parent_2_number = models.CharField(max_length=20, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def calculate_debt(self):
        # 1. Obtener la fecha de inscripción actual del alumno
        enrollment = self.enrollment_date
        
        # 🌟 PARCHE DE SEGURIDAD: Si viene como datetime (con hora), extraemos solo la fecha
        if isinstance(enrollment, datetime.datetime):
            enrollment = enrollment.date()
            
        # 2. Obtener la fecha de hoy limpia (solo año-mes-día)
        hoy = timezone.now().date()
        
        # 3. Calcular los meses transcurridos de forma segura
        days_enrolled = (hoy - enrollment).days
        months_enrolled = max(1, days_enrolled // 30)
        
        # 4. Calcular el total debido acumulado (Ej. $150 por mes)
        total_due = months_enrolled * 150
        
        # 5. Restar lo que el alumno ya pagó en el histórico
        payments = Payment.objects.filter(student=self)
        # Usamos la agregación de Django o un fallback seguro en Decimal
        total_paid = sum(payment.amount for payment in payments)
        
        return Decimal(total_due) - Decimal(total_paid)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Changed default so you can input payments made in the past
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.name} - ${self.amount} on {self.payment_date}"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    # Better to track costs dynamically per course
    monthly_cost = models.DecimalField(max_digits=6, decimal_places=2, default=100.00) 

    def __str__(self):
        return self.name

class CourseClass(models.Model):
    """Renamed from CourseTeacher to represent a specific scheduled offering"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3, choices=DayChoices.choices, default=DayChoices.MONDAY)
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    
    # This replaces CourseTeacherStudent seamlessly using Django's ManyToManyField
    students = models.ManyToManyField(Student, through='Enrollment', related_name='classes')

    def __str__(self):
        return f"{self.course.name} ({self.get_day_of_week_display()}) w/ {self.teacher.name}"

class Enrollment(models.Model):
    """Intermediary table replacing CourseTeacherStudent"""
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    registration_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('course_class', 'student') # Prevents double enrollment in same class

    def __str__(self):
        return f"{self.student.name} in {self.course_class.course.name}"

class Attendance(models.Model):
    # Linked directly to enrollment for tracking
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=False)

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.enrollment.student.name} - {self.enrollment.course_class.course.name}: {status} on {self.date}"