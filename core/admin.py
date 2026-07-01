from django.contrib import admin
from core.models import Student, Payment, Teacher, Course, CourseClass, Enrollment, Attendance

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(CourseClass)
admin.site.register(Enrollment)
admin.site.register(Attendance)
# Register your models here.
