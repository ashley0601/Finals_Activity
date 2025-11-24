from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm, PaymentEditForm
from .models import Courses, Student, Instructor, Enrollment, Grades, Payment


def role_select(request):
    return render(request, 'core/role_select.html')


def student_register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email')
        )
        Student.objects.create(
            user=user,
            student_id=request.POST.get('student_id'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            address=request.POST.get('address')
        )
        login(request, user)
        return redirect('dashboard')
    return render(request, 'core/register_student.html')


def instructor_register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email')
        )
        Instructor.objects.create(
            user=user,
            id_course=request.POST.get('id_course'),
            name=f"{user.first_name} {user.last_name}",
            gender=request.POST.get('gender'),
            subjects=request.POST.get('subjects'),
            email=user.email
        )
        login(request, user)
        return redirect('dashboard')
    return render(request, 'core/register_instructor.html')

@login_required
def student_dashboard(request):
    """Landing page showing only student information"""
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'core/student_dashboard.html', {'student': student})

@login_required
def instructor_list(request):
    """Show instructors and their courses with enroll/unenroll buttons"""
    student = get_object_or_404(Student, user=request.user)
    instructors = Instructor.objects.all()
    
    instructor_data = []
    for instructor in instructors:
        courses = Courses.objects.filter(professor=instructor.name)
        course_data = []
        for course in courses:
            enrollment = Enrollment.objects.filter(
                student=student, 
                course=course
            ).first()
            course_data.append({
                'course': course,
                'is_enrolled': enrollment.status == 'enrolled' if enrollment else False,
                'enrollment_id': enrollment.id if enrollment else None
            })
        instructor_data.append({
            'instructor': instructor,
            'courses': course_data
        })
    
    context = {'student': student, 'instructor_data': instructor_data}
    return render(request, 'core/instructor_list.html', context)

@login_required
def toggle_enrollment(request, instructor_id, course_id):
    """Handle enroll/unenroll toggle"""
    student = get_object_or_404(Student, user=request.user)
    instructor = get_object_or_404(Instructor, id=instructor_id)
    course = get_object_or_404(Courses, id=course_id)
    
    enrollment, created = Enrollment.objects.get_or_create(
        student=student,
        course=course,
        defaults={'status': 'enrolled'}
    )
    
    if not created:
        enrollment.status = 'unenrolled' if enrollment.status == 'enrolled' else 'enrolled'
        enrollment.save()
    
    messages.success(request, f"Successfully {'enrolled in' if enrollment.status == 'enrolled' else 'unenrolled from'} {course.id_course}")
    return redirect('instructor_list')

@login_required
def student_subjects(request):
    """Show read-only subjects, grades and remarks"""
    student = get_object_or_404(Student, user=request.user)
    grades = Grades.objects.filter(student=student)
    
    context = {'student': student, 'grades': grades}
    return render(request, 'core/subjects.html', context)

@login_required
def student_payment(request):
    """Add payment with proper form validation"""
    student = get_object_or_404(Student, user=request.user)
    payments = Payment.objects.filter(student=student)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.save()
            messages.success(request, "Payment added successfully!")
            return redirect('student_payment')
    else:
        form = PaymentForm()
    
    context = {'student': student, 'payments': payments, 'form': form}
    return render(request, 'core/student_payment.html', context)

@login_required
def payment_edit(request, payment_id):
    """Edit existing payment with proper form validation"""
    student = get_object_or_404(Student, user=request.user)
    payment = get_object_or_404(Payment, id=payment_id, student=student)
    
    if request.method == 'POST':
        form = PaymentEditForm(request.POST, instance=payment, instance_id=payment.id)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment updated successfully!")
            return redirect('student_payment')
    else:
        form = PaymentEditForm(instance=payment, instance_id=payment.id)
    
    context = {'student': student, 'form': form, 'payment': payment}
    return render(request, 'core/payment_edit.html', context)

# Modify your existing dashboard function:
@login_required
def dashboard(request):
    """Redirect to appropriate dashboard"""
    if Student.objects.filter(user=request.user).exists():
        return redirect('student_dashboard')
    instructor = get_object_or_404(Instructor, email=request.user.email)
    return render(request, 'core/instructor_dashboard.html', {'instructor': instructor})


@login_required
def instructor_students(request):
    prof_name = request.user.get_full_name()
    courses = Courses.objects.filter(professor=prof_name)
    enrolls = Enrollment.objects.filter(course__in=courses).select_related('student', 'course')
    grades = Grades.objects.filter(professor=prof_name).select_related('student')
    return render(request, 'core/instructor_students.html',
                  {'enrolls': enrolls, 'grades': grades})


@login_required
def grade_edit(request, grade_id):
    grade = get_object_or_404(Grades, pk=grade_id, professor=request.user.get_full_name())
    if request.method == 'POST':
        grade.grades = request.POST.get('grades')
        grade.remarks = request.POST.get('remarks')
        grade.save()
        return redirect('instructor_students')
    return render(request, 'core/grade_edit.html', {'grade': grade})


@login_required
def instructor_profile_edit(request):
    instructor = get_object_or_404(Instructor, email=request.user.email)
    if request.method == 'POST':
        instructor.name = request.POST.get('name')
        instructor.gender = request.POST.get('gender')
        instructor.subjects = request.POST.get('subjects')
        instructor.id_course = request.POST.get('id_course')
        instructor.save()
        return redirect('dashboard')
    return render(request, 'core/instructor_profile_edit.html', {'inst': instructor})


@login_required
def student_edit(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        student.user.first_name = request.POST.get('first_name')
        student.user.last_name = request.POST.get('last_name')
        student.user.save()
        student.student_id = request.POST.get('student_id')
        student.age = request.POST.get('age')
        student.gender = request.POST.get('gender')
        student.address = request.POST.get('address')
        student.save()
        return redirect('dashboard')
    return render(request, 'core/student_edit.html', {'student': student})


@login_required
def student_enroll(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Courses, id_course=course_id)
        Enrollment.objects.create(student=student, course=course)
        return redirect('dashboard')
    all_courses = Courses.objects.all()
    return render(request, 'core/student_enroll.html', {'courses': all_courses})


@login_required
def student_payment(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        Payment.objects.create(
            student=student,
            name=request.POST.get('name'),
            contact_no=request.POST.get('contact_no'),
            password=request.POST.get('password'),
            reference=request.POST.get('reference'),
            method_payment=request.POST.get('method_payment')
        )
        return redirect('dashboard')
    return render(request, 'core/student_payment.html')

