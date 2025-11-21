from django.db import models
from django.contrib.auth.models import User

class Courses(models.Model):
  id_course   = models.CharField(max_length=20, unique=True)
  description = models.CharField(max_length=300)
  subjects    = models.CharField(max_length=100)   # free-text list
  professor   = models.CharField(max_length=100)   # instructor name
  units       = models.IntegerField()

  def __str__(self):
    return self.id_course
  
class Student(models.Model):
  user       = models.OneToOneField(User, on_delete=models.CASCADE)
  student_id = models.CharField(max_length=20, unique=True)
  age        = models.PositiveSmallIntegerField()
  gender     = models.CharField(max_length=10)
  address    = models.TextField()

  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name}"
  
class Enrollment(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
  course  = models.ForeignKey(Courses, on_delete=models.CASCADE)
  date_enrolled = models.DateField(auto_now_add=True)
  status  = models.CharField(max_length=20, default='Pending')

  def __str__(self):
    return f"{self.student} — {self.course.id_course}"
  
class Instructor(models.Model):
  user      = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # optional link
  id_course = models.CharField(max_length=20)
  name      = models.CharField(max_length=100)
  gender    = models.CharField(max_length=10)
  subjects  = models.CharField(max_length=100)
  email     = models.EmailField(unique=True)

  def __str__(self):
    return self.name
  
class Grades(models.Model):
  student   = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
  subjects  = models.CharField(max_length=100)   # mirror of Courses.subjects
  sem_no    = models.IntegerField()
  professor = models.CharField(max_length=100)   # same string as Courses.professor
  grades    = models.IntegerField()
  remarks   = models.CharField(max_length=10)

  def __str__(self):
    return f"{self.student} — {self.subjects}"
  
class Payment(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
  name           = models.CharField(max_length=100)  # payer name
  contact_no     = models.CharField(max_length=20)
  password       = models.CharField(max_length=100)  # gateway pin/hash
  reference      = models.CharField(max_length=50, unique=True)
  method_payment = models.CharField(max_length=50)

  def __str__(self):
    return self.reference
# Create your models here.
