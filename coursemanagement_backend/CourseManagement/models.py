from django.db import models

# Create your models here.
class Department(models.Model):
    DepartmentId = models.AutoField(primary_key=True)  ### The Primary Key
    DepartmentName = models.CharField(max_length=30, null=False)

class Instructor(models.Model):
    InstructorId = models.AutoField(primary_key=True)  ### The Primary Key
    FirstName = models.CharField(max_length=50, null=False)
    LastName = models.CharField(max_length=50, null=False)
    UserName = models.CharField(max_length=50, null=False)
    PassWord = models.CharField(max_length=50, null=False)
    Email = models.EmailField(null=True)
    NRating = models.IntegerField(null=False)  ### The total number of ratings this instructor has, should be updated when student gives rating.
    AverageRating = models.DecimalField(max_digits=4, decimal_places=2, null=True)  ### The average rating this instructor has, should be updated when student gives rating.
    TotalCredit = models.IntegerField(null=False)  ### The total credit hours of courses this instructor teaches, should be updated when instrcutor create/cancel courses.
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)  ### Foreign Key pointing to a department object.

class Course(models.Model):
    CourseId = models.AutoField(primary_key=True)  ### The Primary Key
    Number = models.CharField(max_length=50, null=False)
    Title = models.CharField(max_length=150, null=False)
    Section = models.CharField(max_length=50, null=False)
    Type = models.CharField(max_length=50, null=False)
    CreditHour = models.IntegerField(null=False)
    StartTime = models.CharField(max_length=50, null=False)
    EndTime = models.CharField(max_length=50, null=False)
    DaysOfWeek = models.CharField(max_length=50, null=False)
    Room = models.CharField(max_length=100, null=False)
    Building = models.CharField(max_length=100, null=False)
    Capacity = models.IntegerField(null=False)
    Enrolled = models.IntegerField(null=False)  ### The number of registered student on this course, should be updated when student registers/drops this course.
    NRating = models.IntegerField(null=False)  ### The total number of ratings this course has, should be updated when student gives rating.
    AverageRating = models.DecimalField(max_digits=4, decimal_places=2, null=True)  ### The average rating this instructor has, should be updated when student gives rating.
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)  ### Foreign Key pointing to a department object.
    Instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)  ### Foreign Key pointing to an instructor object.

class Student(models.Model):
    StudentId = models.AutoField(primary_key=True)  ### The Primary Key
    FirstName = models.CharField(max_length=50, null=False)
    LastName = models.CharField(max_length=50, null=False)
    UserName = models.CharField(max_length=50, null=False)
    PassWord = models.CharField(max_length=50, null=False)
    Email = models.EmailField(null=True)
    TotalCredit = models.IntegerField(null=False)  ### The total credit hours of courses this student takes, should be updated when student enrolls/drops courses
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)  ### Foreign Key pointing to a department object
    # Enrollments = models.ManyToManyField(Course, related_name="Enrollments")  ### Foreign Key pointing to a set of course objects.

class Enrollment(models.Model):
    EnrollmentId = models.AutoField(primary_key=True) ### The Primary Key
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)  ### Foreign Key pointing to a student object
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)  ### Foreign Key pointing to a course object

class GiveRating(models.Model):
    RatingId = models.AutoField(primary_key=True)  ### The Primary Key
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)  ### Foreign Key pointing to a student object
    Instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)  ### Foreign Key pointing to an instructor object
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)  ### Foreign Key pointing to a course object
    Rating = models.IntegerField(null=False)  ### Rating should be within [0, 10]
