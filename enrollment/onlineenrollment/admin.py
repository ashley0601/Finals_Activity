from django.contrib import admin

from django.contrib import admin
from .models import *
admin.site.register(Courses)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Enrollment)
admin.site.register(Grades)
admin.site.register(Payment)

# Register your models here.
