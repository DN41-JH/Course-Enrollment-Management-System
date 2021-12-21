from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from CourseManagement.models import Department, Instructor, Student, Course, Enrollment, GiveRating
from CourseManagement.serializers import DepartmentSerializer, InstructorSerializer, StudentSerializer, CourseSerializer
from django.db import connection
import heapq

def executeSQL(sql, arguments=[]):
    with connection.cursor() as cursor:
        try:
            if (sql.startswith("SELECT")):
                if (arguments):
                    print(sql, arguments)
                    cursor.execute(sql, arguments)
                else:
                    cursor.execute(sql)

                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                print(sql, arguments)
                cursor.execute(sql, arguments)
                connection.commit()
        finally:
            cursor.close()

# Create your views here.
class DepartmentsViewSet(viewsets.ViewSet):
    ### get all departments
    # 1. HTTP method: GET;
    # 2. EndPoint URL: /departments
    # 3. User input: No input;
    # 4. Response: return all the departments, 200(OK)
    @csrf_exempt
    @action(detail=False, methods=["GET"])
    def departments(self, request):
        # departments = Department.objects.all() # This returns a list of object that belongs to class "Department"
        # serializer = DepartmentSerializer(departments, many=True) # This convert the python object list "departments" into JSON (Object to Data)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        #################################################################################################################################

        sql = "SELECT * FROM coursemanagement_department"
        departments = executeSQL(sql)
        return Response(departments, status=status.HTTP_200_OK)

    ### get all departments with average rating over all the courses that it offers
    # 1. HTTP method: GET;
    # 2. EndPoint URL: /departmentsRating/
    # 3. User input: No input;
    # 4. Response: return all the departments associated with its average rating over all the courses it offers, 200(OK)
    @csrf_exempt
    @action(detail=False, methods=["GET"])
    def departmentsRating(self, request):
        # departments = Department.objects.all()
        # max_heap = []
        #
        # for department in departments:
        #     department_courses = department.course_set.all()
        #     n_rated_course, totalAverageRating = 0, -1.0
        #
        #     for department_course in department_courses:
        #         if (department_course.AverageRating >= 0):
        #             n_rated_course += 1
        #
        #             if (totalAverageRating == -1.0):
        #                 totalAverageRating = department_course.AverageRating
        #             else:
        #                 totalAverageRating += department_course.AverageRating
        #
        #     serializer = DepartmentSerializer(department, many=False)
        #     department = serializer.data
        #     department["NRating"] = n_rated_course
        #     department["AverageRating"] = -1.0 if (n_rated_course == 0) else float(totalAverageRating / n_rated_course)
        #
        #     heapq.heappush(max_heap, (-department["AverageRating"], -department["NRating"], department["DepartmentId"], department))
        #
        # departments = []
        # while (max_heap):
        #     departments.append(heapq.heappop(max_heap)[3])
        #
        # return Response(departments, status=status.HTTP_200_OK)

        #################################################################################################################################

        sql = """SELECT D.DepartmentId, D.DepartmentName, COUNT(R.RatingId) AS NRating, AVG(R.Rating) AS AverageRating
                   FROM coursemanagement_giverating R JOIN coursemanagement_course C ON (R.Course_id = C.CourseId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)
                   GROUP BY D.DepartmentId, D.DepartmentName
                   ORDER BY AverageRating DESC"""
        departments_withRatings = executeSQL(sql)

        sql = """SELECT DepartmentId, DepartmentName
                   FROM coursemanagement_department WHERE (DepartmentId NOT IN (SELECT D.DepartmentId
                                                                                   FROM coursemanagement_giverating R JOIN coursemanagement_course C ON (R.Course_id = C.CourseId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)))"""
        departments_noRatings = executeSQL(sql)

        return Response(departments_withRatings + departments_noRatings, status=status.HTTP_200_OK)

class StudentsViewSet(viewsets.ViewSet):
    ### obtain all students belong to certain departments or who enroll courses of certain departments
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /students/
    # 3. User input: searchDepartmentNames ---> <String> ---> "CS,ECE,MATH" or "CS"
    # 4. Response: return all the students belong to target departments or who enroll courses of target departments, 200(OK)
    @action(detail=False, methods=["POST"])
    def students(self, request):
        searchDepartmentNames = request.data.get("searchDepartmentNames", None)
        #################################################################################

        # if (not searchDepartmentNames):
        #     students = Student.objects.all()
        #     serializer = StudentSerializer(students, many=True)
        #     students = serializer.data
        #
        #     for student in students:
        #         department = Department.objects.filter(DepartmentId=student["Department"]).first()
        #         student["DepartmentName"] = department.DepartmentName
        #
        #     return Response(students, status=status.HTTP_200_OK)
        #
        # searchDepartmentNames = searchDepartmentNames.split(',')
        # departments = []
        # for searchDepartmentName in searchDepartmentNames:
        #     searchDepartmentName = searchDepartmentName.strip()
        #     department = Department.objects.filter(DepartmentName=searchDepartmentName.upper()).first()
        #
        #     if (not department):
        #         students = Student.objects.none()
        #         serializer = StudentSerializer(students, many=True)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #
        #     departments.append(department)
        #
        # departments_students = set([])
        # departments_courses = set([])
        # for department in departments:
        #     department_students = Student.objects.filter(Department = department)
        #     department_courses = department.course_set.all()
        #
        #     ### Filter students belong to certain departments
        #     for department_student in department_students:
        #         departments_students.add(department_student)
        #
        #     # Filter courses offer by certain departments
        #     for department_course in department_courses:
        #         departments_courses.add(department_course)
        #
        # # Add students who enrolled courses of certain departments
        # for course in department_courses:
        #     course_students = [] # course.Enrollments.all()
        #     enrollments = Enrollment.objects.filter(Course = course)
        #     for enrollment in enrollments:
        #         course_students.append(Student.objects.filter(StudentId = enrollment.Student.StudentId).first())
        #
        #     for student in course_students:
        #         departments_students.add(student)
        #
        # serializer = StudentSerializer(list(departments_students), many=True)
        # departments_students = serializer.data
        #
        # for departments_student in departments_students:
        #     department = Department.objects.filter(DepartmentId=departments_student["Department"]).first()
        #     departments_student["DepartmentName"] = department.DepartmentName
        #
        # return Response(departments_students, status=status.HTTP_200_OK)

        #################################################################################################################################

        if (not searchDepartmentNames):
            sql = "SELECT S.*, D.DepartmentName FROM coursemanagement_student S JOIN coursemanagement_department D ON (S.Department_id = D.DepartmentId)"
            students = executeSQL(sql)

            return Response(students, status=status.HTTP_200_OK)

        searchDepartmentNames = searchDepartmentNames.split(',')
        departments = []
        for searchDepartmentName in searchDepartmentNames:
            searchDepartmentName = searchDepartmentName.strip()
            if (not searchDepartmentName):
                continue

            sql = "SELECT * FROM coursemanagement_department D WHERE D.DepartmentName = %s"
            department = executeSQL(sql, [searchDepartmentName])
            if (not department):
                students = []
                return Response(students, status=status.HTTP_200_OK)

            departments.append(department[0])

        departments_students = []
        for department in departments:
            sql = """SELECT S.FirstName, S.LastName, S.TotalCredit, D.DepartmentName
                        FROM coursemanagement_student S JOIN coursemanagement_enrollment E ON (S.StudentId=E.Student_id) JOIN coursemanagement_course C ON (C.CourseId=E.Course_id) JOIN coursemanagement_department D ON (D.DepartmentId=S.Department_id)
                        WHERE (C.Department_id=%s)
                        UNION
                        SELECT S1.FirstName, S1.LastName, S1.TotalCredit, D1.DepartmentName
                        FROM coursemanagement_student S1 JOIN coursemanagement_department D1 ON (S1.Department_id=D1.DepartmentId)
                        WHERE S1.Department_id=%s"""
            students = executeSQL(sql, [department["DepartmentId"], department["DepartmentId"]])
            for student in students:
                if (student not in departments_students):
                    departments_students.append(student)

        return Response(departments_students, status=status.HTTP_200_OK)

class InstructorsViewSet(viewsets.ViewSet):
    ### obtain all instructors
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /instructors/
    # 3. User input: searchInstructorFirstName, searchInstructorLastName, searchInstructorDepartment
    # 4. Response: return all the instructors or searching instructors (if required), 200(OK)
    @action(detail=False, methods=["POST"])
    def instructors(self, request):
        searchInstructorFirstName = request.data.get("searchInstructorFirstName", None)
        searchInstructorLastName = request.data.get("searchInstructorLastName", None)
        searchInstructorDepartment = request.data.get("searchInstructorDepartment", None)
        doSearchDepartment = True if (searchInstructorDepartment) else False
        ######################################################################################

        department = Department.objects.filter(DepartmentName=searchInstructorDepartment).first()

        if (doSearchDepartment):
            if (department):
                if (searchInstructorFirstName and searchInstructorLastName):
                    instructors = Instructor.objects.filter(FirstName=searchInstructorFirstName, LastName=searchInstructorLastName, Department=department)
                elif (searchInstructorFirstName):
                    instructors = Instructor.objects.filter(FirstName=searchInstructorFirstName, Department=department)
                elif (searchInstructorLastName):
                    instructors = Instructor.objects.filter(LastName=searchInstructorLastName, Department=department)
                else:
                    instructors = Instructor.objects.filter(Department=department)
            else:
                instructors = Instructor.objects.none()

        else:
            if (searchInstructorFirstName and searchInstructorLastName):
                instructors = Instructor.objects.filter(FirstName=searchInstructorFirstName, LastName=searchInstructorLastName)
            elif (searchInstructorFirstName):
                instructors = Instructor.objects.filter(FirstName=searchInstructorFirstName)
            elif (searchInstructorLastName):
                instructors = Instructor.objects.filter(LastName=searchInstructorLastName)
            else:
                instructors = Instructor.objects.all()

        serializer = InstructorSerializer(instructors, many=True)
        instructors = serializer.data

        for instructor in instructors:
            department = Department.objects.filter(DepartmentId=instructor["Department"]).first()
            instructor['DepartmentName'] = department.DepartmentName

        return Response(instructors, status=status.HTTP_200_OK)

        #################################################################################################################################

        # sql = "SELECT * FROM coursemanagement_department WHERE DepartmentName = %s"
        # department = executeSQL(sql, [searchInstructorDepartment])
        #
        # if (doSearchDepartment):
        #     if (department):
        #         department = department[0]
        #
        #         if (searchInstructorFirstName and searchInstructorLastName):
        #             sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                         FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                         WHERE (I.Department_id = %s AND I.FirstName = %s AND I.LastName = %s)"""
        #             instructors = executeSQL(sql, [department["DepartmentId"], searchInstructorFirstName.lower(), searchInstructorLastName.lower()])
        #         elif (searchInstructorFirstName):
        #             sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                         FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                         WHERE (I.Department_id = %s AND I.FirstName = %s)"""
        #             instructors = executeSQL(sql, [department["DepartmentId"], searchInstructorFirstName.lower()])
        #         elif (searchInstructorLastName):
        #             sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                         FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                         WHERE (I.Department_id = %s AND I.LastName = %s)"""
        #             instructors = executeSQL(sql, [department["DepartmentId"], searchInstructorLastName.lower()])
        #         else:
        #             sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                         FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                         WHERE (I.Department_id = %s)"""
        #             instructors = executeSQL(sql, [department["DepartmentId"]])
        #     else:
        #         sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                    FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                    WHERE (1 = 0)"""
        #         instructors = []
        #
        # else:
        #     if (searchInstructorFirstName and searchInstructorLastName):
        #         sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                     FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                     WHERE (I.FirstName = %s AND I.LastName = %s)"""
        #         instructors = executeSQL(sql, [searchInstructorFirstName.lower(), searchInstructorLastName.lower()])
        #     elif (searchInstructorFirstName):
        #         sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                     FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                     WHERE (I.FirstName = %s)"""
        #         instructors = executeSQL(sql, [searchInstructorFirstName.lower()])
        #     elif (searchInstructorLastName):
        #         sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                     FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)
        #                     WHERE (I.LastName = %s)"""
        #         instructors = executeSQL(sql, [searchInstructorLastName.lower()])
        #     else:
        #         sql = """SELECT I.FirstName, I.LastName, I.AverageRating, D.DepartmentName
        #                     FROM coursemanagement_instructor I JOIN coursemanagement_department D ON (I.Department_id = D.DepartmentId)"""
        #         instructors = executeSQL(sql)
        #
        # return Response(instructors, status=status.HTTP_200_OK)

class CoursesViewSet(viewsets.ViewSet):
    ### get all courses
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /courses/
    # 3. User input: searchCourseNumber, searchInstructorFirstName, searchInstructorLastName;
    # 4. Response: return all the courses or searching courses (if required), 200(OK)
    @action(detail=False, methods=["POST"])
    def courses(self, request):
        searchCourseNumber = request.data.get("searchCourseNumber", None)
        searchInstructorFirstName = request.data.get("searchInstructorFirstName", None)
        searchInstructorLastName = request.data.get("searchInstructorLastName", None)
        doSearchInstructor = searchInstructorFirstName or searchInstructorLastName
        instructor = None
        ##################################################################################

        # if (searchInstructorFirstName and searchInstructorLastName):
        #     instructor = Instructor.objects.filter(FirstName=searchInstructorFirstName, LastName=searchInstructorLastName).first()
        # elif (searchInstructorFirstName):
        #     instructor = Instructor.objects.filter(FirstName=searchInstructorFirstName).first()
        # elif (searchInstructorLastName):
        #     instructor = Instructor.objects.filter(LastName=searchInstructorLastName).first()
        #
        # if (doSearchInstructor):
        #     if (instructor and searchCourseNumber):
        #         courses = Course.objects.filter(Number__istartswith=searchCourseNumber, Instructor=instructor)
        #     elif (instructor):
        #         courses = Course.objects.filter(Instructor=instructor)
        #     else:
        #         courses = Course.objects.none()
        #
        # else:
        #     if (searchCourseNumber):
        #         courses = Course.objects.filter(Number__istartswith=searchCourseNumber)
        #     else:
        #         courses = Course.objects.all()
        #
        # serializer = CourseSerializer(courses, many=True)
        # courses = serializer.data
        #
        # for course in courses:
        #     instructor = Instructor.objects.filter(InstructorId=course["Instructor"]).first()
        #     department = Department.objects.filter(DepartmentId=course["Department"]).first()
        #     course['InstructorName'] = ''.join([instructor.FirstName, ' ', instructor.LastName])
        #     course['DepartmentName'] = department.DepartmentName
        #
        # return Response(courses, status=status.HTTP_200_OK)

        #################################################################################################################################

        if (searchInstructorFirstName and searchInstructorLastName):
            sql = "SELECT * FROM coursemanagement_instructor I WHERE (I.FirstName = %s AND I.LastName = %s)"
            instructor = executeSQL(sql, [searchInstructorFirstName, searchInstructorLastName])
        elif (searchInstructorFirstName):
            sql = "SELECT * FROM coursemanagement_instructor I WHERE (I.FirstName = %s)"
            instructor = executeSQL(sql, [searchInstructorFirstName])
        elif (searchInstructorLastName):
            sql = "SELECT * FROM coursemanagement_instructor I WHERE (I.LastName = %s)"
            instructor = executeSQL(sql, [searchInstructorLastName])

        if (doSearchInstructor):
            if (instructor and searchCourseNumber):
                instructor = instructor[0]
                sql = """SELECT C.*, I.FirstName, I.LastName, D.DepartmentName
                            FROM coursemanagement_course C JOIN coursemanagement_instructor I ON (C.Instructor_id = I.InstructorId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)
                            WHERE (C.Number LIKE %s AND I.InstructorId = %s)"""
                courses = executeSQL(sql, [searchCourseNumber + '%', instructor["InstructorId"]])
            elif (instructor):
                instructor = instructor[0]
                sql = """SELECT C.*, I.FirstName, I.LastName, D.DepartmentName
                            FROM coursemanagement_course C JOIN coursemanagement_instructor I ON (C.Instructor_id = I.InstructorId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)
                            WHERE (I.InstructorId = %s)"""
                courses = executeSQL(sql, [instructor["InstructorId"]])
            else:
                sql = """SELECT C.*, I.FirstName, I.LastName, D.DepartmentName
                            FROM coursemanagement_course C JOIN coursemanagement_instructor I ON (C.Instructor_id = I.InstructorId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)
                            WHERE (1 = 0)"""
                courses = []

        else:
            if (searchCourseNumber):
                sql = """SELECT C.*, I.FirstName, I.LastName, D.DepartmentName
                            FROM coursemanagement_course C JOIN coursemanagement_instructor I ON (C.Instructor_id = I.InstructorId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)
                            WHERE (C.Number LIKE %s)"""
                courses = executeSQL(sql, [searchCourseNumber + '%'])
            else:
                sql = """SELECT C.*, I.FirstName, I.LastName, D.DepartmentName
                            FROM coursemanagement_course C JOIN coursemanagement_instructor I ON (C.Instructor_id = I.InstructorId) JOIN coursemanagement_department D ON (C.Department_id = D.DepartmentId)"""
                courses = executeSQL(sql)

        return Response(courses, status=status.HTTP_200_OK)

class RegistrationViewSet(viewsets.ViewSet):
    ### check the status of a user (either student or instructor)
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /checkStatus/
    # 3. User input: ID, Role
    # 4. Response: return the TotalCredit of the requesting user, 200(OK)
    @action(detail=False, methods=["POST"])
    def checkStatus(self, request):
        ID = request.data.get('ID', None)
        Role = request.data.get('Role', None)

        if (not ID):
            return Response({"response": {"error":"You Are Not Logged In."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        if (not Role):
            return Response({"response": {"error":"User Role Not Specified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        if (Role == "Student"):
            student = Student.objects.filter(StudentId=ID).first()
            if (student):
                departmentName = student.Department.DepartmentName
                serializer = StudentSerializer(student, many=False)
                student = serializer.data
                student["DepartmentName"] = departmentName

                return Response(student, status=status.HTTP_200_OK)
            else:
                return Response({"response": {"error":"Student Not Specified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        elif (Role == "Instructor"):
            instructor = Instructor.objects.filter(InstructorId=ID).first()
            if (instructor):
                departmentName = instructor.Department.DepartmentName
                serializer = InstructorSerializer(instructor, many=False)
                instructor = serializer.data
                instructor["DepartmentName"] = departmentName

                return Response(instructor, status=status.HTTP_200_OK)
            else:
                Response({"response": {"error":"Instructor Not Specified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"response": {"error":"User Role Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### register a new user (either student or instructor)
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /register/
    # 3. User input: FirstName, LastName, UserName, PassWord, Email, Role, DepartmentName
    # 4. Response: empty content, 201(CREATED);
    @action(detail=False, methods=["POST"])
    def register(self, request):
        UserName = request.data.get('UserName', None)
        PassWord = request.data.get('PassWord', None)
        Email = request.data.get('Email', None)
        FirstName = request.data.get('FirstName', None)
        LastName = request.data.get('LastName', None)
        Role = request.data.get('Role', None)
        DepartmentName = request.data.get('DepartmentName', None)

        if (DepartmentName is None):
            return Response({"response": {"error":"User's Department Not Specified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        department = Department.objects.filter(DepartmentName=DepartmentName).first()
        if (not department):
            return Response({"response": {"error":"Unknown User's Associated Department"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        doExist_student = Student.objects.filter(UserName=UserName).first()
        doExist_instructor = Instructor.objects.filter(UserName=UserName).first()

        if (Role == "Student"):
            if (doExist_student):
                return Response({"response": {"error":"Student Already Existed."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            elif (doExist_instructor):
                return Response({"response": {"error":"UserName Already Taken by One of the Instructors."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                newStudent = Student(UserName=UserName, PassWord=PassWord, Email=Email, FirstName=FirstName, LastName=LastName, TotalCredit=0, Department=department)
                newStudent.save()

                return Response({"response": {"message":"New Student Created"}, "status": 201}, status=status.HTTP_201_CREATED)
        elif (Role == "Instructor"):
            if (doExist_instructor):
                return Response({"response": {"error":"Instructor Already Existed."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            elif (doExist_student):
                return Response({"response": {"error":"UserName Already Taken by One of the Students."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                newInstructor = Instructor(UserName=UserName, PassWord=PassWord, Email=Email, FirstName=FirstName, LastName=LastName, NRating=0, AverageRating=-1.0, TotalCredit=0, Department=department)
                newInstructor.save()

                return Response({"response": {"message":"New Instructor Created"}, "status": 201}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": {"error":"Unknown User Type."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### withdraw a user from the system
    # 1. HTTP method: DELETE;
    # 2. EndPoint URL: /withdraw/
    # 3. User input: ID, Role
    # 4. Response: empty content, 202(ACCEPTED)
    @action(detail=False, methods=["DELETE"])
    def withdraw(self, request):
        ID = request.data.get('ID', None)
        Role = request.data.get('Role', None)

        if (ID is None):
            return Response({"response": {"error":"Missing User ID."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        if (Role is None):
            return Response({"response": {"error":"Missing User Role."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        if (Role == "Student"):
            student = Student.objects.filter(StudentId=ID).first()

            if (student):
                student_courses = [] # student.Enrollments.all()
                enrollments = Enrollment.objects.filter(Student=student)
                for enrollment in enrollments:
                    student_courses.append(Course.objects.filter(CourseId=enrollment.Course.CourseId).first())

                if (student_courses):
                    return Response({"response": {"error":"Please drop all enrolled courses before withdraw."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    student.delete()
                    return Response({"response": {"message":"Student User Deleted."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response": {"error":"Un-identified Student User."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        elif (Role == "Instructor"):
            instructor = Instructor.objects.filter(InstructorId=ID).first()

            if (instructor):
                instructor_courses = instructor.course_set.all()
                if (instructor_courses):
                    return Response({"response": {"error":"Please cancel all your courses before withdraw."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    instructor.delete()
                    return Response({"response": {"message":"Instructor User Deleted."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response": {"error":"Un-identified Instructor User."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"response": {"error":"Unknown User Role."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.ViewSet):
    ### handle the login request from user
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /login/
    # 3. User input: UserName, PassWord
    # 4. Response: ID, Name, Role;
    @action(detail=False, methods=["POST"])
    def login(self, request):
        UserName = request.data.get('UserName', None)
        PassWord = request.data.get('PassWord', None)

        if (UserName is None):
            return Response({"response": {"error":"UserName Not Specified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        if (PassWord is None):
            return Response({"response": {"error":"PassWord Not Specified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(UserName=UserName, PassWord=PassWord).first()
        instructor = Instructor.objects.filter(UserName=UserName, PassWord=PassWord).first()

        if (student):
            return Response({"response": {"ID":student.StudentId, "Role":"Student"}, "status": 200}, status=status.HTTP_200_OK)
        elif (instructor):
            return Response({"response": {"ID":instructor.InstructorId, "Role":"Instructor"}, "status":200}, status=status.HTTP_200_OK)
        else:
            return Response({"response": {"error":"Incorrect UserName or PassWord."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

class InstructorViewSet(viewsets.ViewSet):
    ### obtain all the courses taught by the Instructor
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /instructor/courses/
    # 3. User input: InstructorId
    # 4. Response: return all the courses taught by the instructor, 200(OK)
    @action(detail=False, methods=["POST"])
    def courses(self, request):
        ID = request.data.get("InstructorId", None)
        #############################################################

        # instructor = Instructor.objects.filter(InstructorId=ID).first()
        # if (instructor):
        #     instructor_courses = instructor.course_set.all()
        #     serializer = CourseSerializer(instructor_courses, many=True) # This convert the python object list "courses" into JSON (Object to Data)
        #     instructor_courses = serializer.data
        #
        #     for instructor_course in instructor_courses:
        #         instructor = Instructor.objects.filter(InstructorId=instructor_course["Instructor"]).first()
        #         department = Department.objects.filter(DepartmentId=instructor_course["Department"]).first()
        #         instructor_course['FirstName'] = instructor.FirstName
        #         instructor_course['LastName'] = instructor.LastName
        #         instructor_course['DepartmentName'] = department.DepartmentName
        #
        #     return Response(instructor_courses, status=status.HTTP_200_OK)
        # else:
        #     return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        #################################################################################################################################

        sql = "SELECT * FROM coursemanagement_instructor I WHERE (I.InstructorId = %s)"
        instructor = executeSQL(sql, [ID])[0]

        if (instructor):
            sql = """SELECT I.FirstName, I.LastName, C.*
                        FROM coursemanagement_instructor I JOIN coursemanagement_course C ON (I.InstructorId=C.Instructor_id)
                        WHERE C.Instructor_id = %s"""
            instructor_courses = executeSQL(sql, [instructor['InstructorId']])

            return Response(instructor_courses, status=status.HTTP_200_OK)
        else:
            return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### obtain all the students enrolled on the course taught by the instructor
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /instructor/students/
    # 3. User input: InstructorId, CourseId
    # 4. Response: return all the student enrolled on the course if the course is taught by the instructor, 200(OK)
    @action(detail=False, methods=["POST"])
    def students(self, request):
        InstructorId = request.data.get("InstructorId", None)
        CourseId = request.data.get("CourseId", None)
        ##################################################################

        # course = Course.objects.filter(CourseId=CourseId).first()
        # if (not course):
        #     return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # instructor = Instructor.objects.filter(InstructorId=InstructorId).first()
        # if (instructor):
        #     if (course in instructor.course_set.all()):
        #         course_students = [] # course.Enrollments.all()
        #         enrollments = Enrollment.objects.filter(Course=course)
        #         for enrollment in enrollments:
        #             course_students.append(Student.objects.filter(StudentId=enrollment.Student.StudentId).first())
        #
        #         serializer = StudentSerializer(course_students, many=True)
        #         course_students = serializer.data
        #
        #         for course_student in course_students:
        #             department = Department.objects.filter(DepartmentId=course_student["Department"]).first()
        #             course_student["DepartmentName"] = department.DepartmentName
        #
        #         return Response(course_students, status=status.HTTP_200_OK)
        #     else:
        #         return Response({"response": {"error":"Course Not Taught by the Instructor."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # else:
        #     return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        #################################################################################################################################

        sql = "SELECT * FROM coursemanagement_course C WHERE C.CourseId=%s"
        course = executeSQL(sql, [CourseId])
        if (not course):
            return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        course = course[0]

        sql = "SELECT * FROM coursemanagement_instructor I WHERE I.InstructorId=%s"
        instructor = executeSQL(sql, [InstructorId])
        if (instructor):
            instructor = instructor[0]
            sql = """SELECT C.*
                        FROM coursemanagement_course C JOIN coursemanagement_instructor I ON (I.InstructorId=C.Instructor_id)
                        WHERE I.InstructorId=%s"""
            instructor_courses = executeSQL(sql, [instructor["InstructorId"]])

            if (course in instructor_courses):
                sql = """SELECT S.*, D.DepartmentName
                            FROM coursemanagement_student S JOIN coursemanagement_enrollment E ON (S.StudentId=E.Student_id) JOIN coursemanagement_course C ON (C.CourseId=E.Course_id) JOIN coursemanagement_department D ON (D.DepartmentId=S.Department_id)
                            WHERE C.CourseId=%s"""
                course_students = executeSQL(sql, [course["CourseId"]])

                return Response(course_students, status=status.HTTP_200_OK)
            else:
                return Response({"response": {"error":"Course Not Taught By the Instructor."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### create a course taught by the Instructor
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /instructor/createCourse/
    # 3. User input: Number, Title, Section, Type, CreditHour, StartTime, EndTime, DaysOfWeek, Room, Building, Capacity, InstructorId
    # 4. Response: empty content, 201(CREATED);
    @action(detail=False, methods=["POST"])
    def createCourse(self, request):
        Number = request.data.get('Number', None)
        Title = request.data.get('Title', None)
        Section = request.data.get('Section', None)
        Type = request.data.get('Type', None)
        CreditHour = request.data.get('CreditHour', 0)
        StartTime = request.data.get('StartTime', None)
        EndTime = request.data.get('EndTime', None)
        DaysOfWeek = request.data.get('DaysOfWeek', None)
        Room = request.data.get('Room', None)
        Building = request.data.get('Building', None)
        Capacity = request.data.get('Capacity', None)
        InstructorId = request.data.get('InstructorId', None)
        ########################################################################

        instructor = Instructor.objects.filter(InstructorId=InstructorId).first()
        if (not instructor):
            return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        doExist = Course.objects.filter(Number=Number, Section=Section).first()
        if (doExist):
            return Response({"response": {"error":"The Same Section of the Same Course Already Existed."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        ############################ Course Time&Place Overlapping Check Goes Here ################################

        if (CreditHour < 0):
            return Response({"response": {"error":"Course Credit Hour Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        if (Capacity < 0):
            return Response({"response": {"error":"Course Maximum Capacity Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        newCourse = Course(Number=Number, Title=Title, Section=Section, Type=Type, CreditHour=CreditHour, StartTime=StartTime, EndTime=EndTime, DaysOfWeek=DaysOfWeek, Room=Room, Building=Building, Capacity=Capacity, Enrolled=0, NRating=0, AverageRating=-1.0, Department=instructor.Department, Instructor=instructor)
        newCourse.save()
        instructor.TotalCredit += CreditHour
        instructor.save()

        return Response({"response": {"message":"New Course Created"}, "status": 201}, status=status.HTTP_201_CREATED)

        ###################################################################################################################################################################

        # sql = "SELECT * FROM coursemanagement_instructor WHERE InstructorId = %s"
        # instructor = executeSQL(sql, [InstructorId])
        # if (not instructor):
        #     return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        # instructor = instructor[0]
        #
        # sql = "SELECT * FROM coursemanagement_course WHERE Number = %s AND Section = %s"
        # doExist = executeSQL(sql, [Number, Section])
        # if (doExist):
        #     return Response({"response": {"error":"The Same Section of the Same Course Already Existed."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # if (CreditHour < 0):
        #     return Response({"response": {"error":"Course Credit Hour Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        # if (Capacity < 0):
        #     return Response({"response": {"error":"Course Maximum Capacity Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # sql = """INSERT INTO coursemanagement_course(Number, Title, Section, Type, CreditHour, StartTime, EndTime, DaysOfWeek, Room, Building, Capacity, Enrolled, NRating, AverageRating, Department_id, Instructor_id)
        #             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # executeSQL(sql, [Number, Title, Section, Type, CreditHour, StartTime, EndTime, DaysOfWeek, Room, Building, Capacity, 0, 0, -1.0, instructor["Department_id"], InstructorId])
        #
        # sql = "UPDATE coursemanagement_instructor SET TotalCredit = %s WHERE InstructorId = %s"
        # executeSQL(sql, [instructor["TotalCredit"] + CreditHour, InstructorId])
        #
        # return Response({"response": {"message":"New Course Created"}, "status": 201}, status=status.HTTP_201_CREATED)

    ### update a course taught by the Instructor
    # 1. HTTP method: PUT;
    # 2. EndPoint URL: /instructor/updateCourse/
    # 3. User Input: CourseId, InstructorId, TargetField (Number/Title/Section/Type/CreditHour/StartTime/EndTime/DaysOfWeek/Room/Building/Capacity), NewContent
    # 4. Response: empty content, 202(ACCEPTED)
    @action(detail=False, methods=["PUT"])
    def updateCourse(self, request):
        CourseId = request.data.get('CourseId', None)
        InstructorId = request.data.get('InstructorId', None)
        TargetField = request.data.get('TargetField', None)
        NewContent = request.data.get('NewContent', None)

        if (not TargetField):
            return Response({"response": {"error": "Please Specify the Course Field to Update"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        if (not NewContent):
            return Response({"response": {"error": "Please Enter the Updated Content."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        ##########################################################################################################################################

        # instructor = Instructor.objects.filter(InstructorId=InstructorId).first()
        # if (not instructor):
        #     return Response({"response": {"error": "Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # course = Course.objects.filter(CourseId=CourseId).first()
        # if (not course):
        #     return Response({"response": {"error": "Course Not Identified"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # if (course not in instructor.course_set.all()):
        #     return Response({"response": {"error": "Course Not Taught by the Instructor."}, 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # ### Starts checking and updating the target field
        # if (TargetField.lower() == "course"):
        #     if (NewContent == course.Number):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.Number = NewContent
        #
        # elif (TargetField.lower() == "title"):
        #     if (NewContent == course.Title):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.Title = NewContent
        #
        # elif (TargetField.lower() == "section"):
        #     if (NewContent == course.Section):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.Section = NewContent
        #
        # elif (TargetField.lower() == "type"):
        #     if (NewContent == course.Type):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.Type = NewContent
        #
        # elif (TargetField.lower() == "starttime"):
        #     if (NewContent == course.StartTime):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     if (NewContent > course.EndTime):
        #         return Response({"response": {"error": "Course Start Time Cannot Be Later Than Stop Time"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.StartTime = NewContent
        #
        # elif (TargetField.lower() == "endtime"):
        #     if (NewContent == course.EndTime):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     if (NewContent < course.StartTime):
        #         return Response({"response": {"error": "Course End Time Cannot Be Earlier Than Start Time"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.EndTime = NewContent
        #
        # elif (TargetField.lower() == "days"):
        #     if (NewContent == course.DaysOfWeek):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.DaysOfWeek = NewContent
        #
        # elif (TargetField.lower() == "room"):
        #     if (NewContent == course.Room):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.Room = NewContent
        #
        # elif (TargetField.lower() == "building"):
        #     if (NewContent == course.Building):
        #         return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #     course.Building = NewContent
        #
        # elif (TargetField.lower() == "capacity"):
        #     try:
        #         NewContent = int(NewContent)
        #
        #         if (NewContent < 0):
        #             return Response({"response": {"error": "Course Maximum Capacity Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #         if (NewContent == course.Capacity):
        #             return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #         if (NewContent < course.Enrolled):
        #             return Response({"response": {"error": "Course Maximum Capacity Cannot be Less Than Current Enrollments."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #         course.Capacity = NewContent
        #     except:
        #         return Response({"response": {"error": "Course Maximum Capacity Must be Integer."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # elif (TargetField.lower() == "credithour"):
        #     try:
        #         NewContent = int(NewContent)
        #
        #         if (NewContent < 0):
        #             return Response({"response": {"error": "Course Credit Hour Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #         if (NewContent == course.CreditHour):
        #             return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        #         old_CreditHour = course.CreditHour
        #         instructor.TotalCredit = instructor.TotalCredit - old_CreditHour + NewContent
        #         instructor.save()
        #
        #         course_students = []
        #         enrollments = Enrollment.objects.filter(Course=course)
        #         for enrollment in enrollments:
        #             course_students.append(Student.objects.filter(StudentId=enrollment.Student.StudentId).first())
        #
        #         for student in course_students:
        #             student.TotalCredit = student.TotalCredit - old_CreditHour + NewContent
        #             student.save()
        #         course.CreditHour = NewContent
        #     except:
        #         return Response({"response": {"error": "Course Credit Hour Must be Integer."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # else:
        #     return Response({"response": {"error": "Course Field Not Identified."}, 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # course.save()
        # return Response({"response": {"message":"Rating Successfully Recorded."}, "status": 202}, status=status.HTTP_202_ACCEPTED)

        #################################################################################################################################

        sql = "SELECT * FROM coursemanagement_instructor I WHERE I.InstructorId = %s"
        instructor = executeSQL(sql, [InstructorId])
        if (not instructor):
            return Response({"response": {"error": "Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        instructor = instructor[0]

        sql = "SELECT * FROM coursemanagement_course C WHERE C.CourseId = %s"
        course = executeSQL(sql, [CourseId])
        if (not course):
            return Response({"response": {"error": "Course Not Identified"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        course = course[0]

        sql = "SELECT C.* FROM coursemanagement_instructor I JOIN coursemanagement_course C ON (C.Instructor_id = %s)"
        instructor_courses = executeSQL(sql, [InstructorId])
        if (course not in instructor_courses):
            return Response({"response": {"error": "Course Not Taught by the Instructor."}, 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        sql = None
        ### Starts checking and updating the target field
        if (TargetField.lower() == "course"):
            if (NewContent == course["Number"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET Number = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "title"):
            if (NewContent == course["Title"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET Title = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "section"):
            if (NewContent == course["Section"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET Section = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "type"):
            if (NewContent == course["Type"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET Type = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "starttime"):
            if (NewContent == course["StartTime"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            if (NewContent > course["EndTime"]):
                return Response({"response": {"error": "Course Start Time Cannot Be Later Than Stop Time"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET StartTime = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "endtime"):
            if (NewContent == course["EndTime"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            if (NewContent < course["StartTime"]):
                return Response({"response": {"error": "Course End Time Cannot Be Earlier Than Start Time"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET EndTime = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "days"):
            if (NewContent == course["DaysOfWeek"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET DaysOfWeek = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "room"):
            if (NewContent == course["Room"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET Room = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "building"):
            if (NewContent == course["Building"]):
                return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            sql = "UPDATE coursemanagement_course SET Building = %s WHERE CourseId = %s"

        elif (TargetField.lower() == "capacity"):
            try:
                NewContent = int(NewContent)

                if (NewContent < 0):
                    return Response({"response": {"error": "Course Maximum Capacity Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                if (NewContent == course["Capacity"]):
                    return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                if (NewContent < course["Enrolled"]):
                    return Response({"response": {"error": "Course Maximum Capacity Cannot be Less Than Current Enrollments."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                sql = "UPDATE coursemanagement_course SET Capacity = %s WHERE CourseId = %s"
            except:
                return Response({"response": {"error": "Course Maximum Capacity Must be Integer."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        elif (TargetField.lower() == "credithour"):
            try:
                NewContent = int(NewContent)

                if (NewContent < 0):
                    return Response({"response": {"error": "Course Credit Hour Cannot be Negative."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                if (NewContent == course["CreditHour"]):
                    return Response({"response": {"error": "No changes deteced"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

                old_CreditHour = course["CreditHour"]

                sql_sp = "UPDATE coursemanagement_instructor SET TotalCredit = %s WHERE InstructorId = %s"
                executeSQL(sql_sp, [instructor["TotalCredit"] - old_CreditHour + NewContent, InstructorId])

                sql_sp = "SELECT S.* FROM coursemanagement_student S JOIN coursemanagement_enrollment E ON (E.Student_id=S.StudentId) WHERE E.Course_id = %s"
                course_students = executeSQL(sql_sp, [CourseId])
                for student in course_students:
                    sql_sp = "UPDATE coursemanagement_student SET TotalCredit = %s WHERE StudentId = %s"
                    executeSQL(sql_sp, [student["TotalCredit"] - old_CreditHour + NewContent, student["StudentId"]])
                sql = "UPDATE coursemanagement_course SET CreditHour = %s WHERE CourseId = %s"
            except:
                return Response({"response": {"error": "Course Credit Hour Must be Integer."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"response": {"error": "Course Field Not Identified."}, 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        if (sql):
            executeSQL(sql, [NewContent, CourseId])
        return Response({"response": {"message":"Successfully Updated the Course."}, "status": 202}, status=status.HTTP_202_ACCEPTED)

    ### delete a course taught by the Instructor
    # 1. HTTP method: DELETE;
    # 2. EndPoint URL: /instructor/deleteCourse/
    # 3. User Input: InstructorId, CourseId
    # 4. Response: empty content, 202(ACCEPTED)
    @action(detail=False, methods=["DELETE"])
    def deleteCourse(self, request):
        InstructorId = request.data.get("InstructorId", None)
        CourseId = request.data.get("CourseId", None)
        #########################################################

        instructor = Instructor.objects.filter(InstructorId=InstructorId).first()
        if (instructor):
            instructor_courses = instructor.course_set.all()
            course = Course.objects.filter(CourseId=CourseId).first()

            if (course):
                if (course in instructor_courses):
                    instructor.TotalCredit -= course.CreditHour
                    instructor.save()

                    course_students = []
                    enrollments = Enrollment.objects.filter(Course=course)
                    for enrollment in enrollments:
                        course_students.append(Student.objects.filter(StudentId=enrollment.Student.StudentId).first())

                    for student in course_students:
                        student.TotalCredit -= course.CreditHour
                        student.save()

                    course.delete()
                    return Response({"response": {"message":"Student User Deleted."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"response": {"error":"The Instructor Doesn't Teach the Course."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        #################################################################################################################################

        # sql = "SELECT * FROM coursemanagement_instructor WHERE InstructorId = %s"
        # instructor = executeSQL(sql, [InstructorId])
        # if (instructor):
        #     instructor = instructor[0]
        #
        #     sql = "SELECT * FROM coursemanagement_course C WHERE C.Instructor_id = %s"
        #     instructor_courses = executeSQL(sql, [InstructorId])
        #
        #     sql = "SELECT * FROM coursemanagement_course C WHERE C.CourseId = %s"
        #     course = executeSQL(sql, [CourseId])
        #     if (course):
        #         course = course[0]
        #
        #         if (course in instructor_courses):
        #             sql = """SELECT S.StudentId, S.TotalCredit
        #                         FROM coursemanagement_student S JOIN coursemanagement_enrollment E ON S.StudentId = E.student_id
        #                         WHERE E.course_id = %s"""
        #             course_students = executeSQL(sql, [CourseId])
        #
        #             for course_student in course_students:
        #                 sql = "UPDATE coursemanagement_student SET TotalCredit = %s WHERE StudentId = %s"
        #                 executeSQL(sql, [course_student["TotalCredit"] - course["CreditHour"], course_student["StudentId"]])
        #                 sql = "DELETE FROM coursemanagement_enrollment WHERE Student_id = %s AND Course_id = %s"
        #                 executeSQL(sql, [course_student["StudentId"], CourseId])
        #
        #             sql = "UPDATE coursemanagement_instructor SET TotalCredit = %s WHERE InstructorId = %s"
        #             executeSQL(sql, [instructor["TotalCredit"] - course["CreditHour"], InstructorId])
        #
        #             sql = "SET FOREIGN_KEY_CHECKS = %s"
        #             executeSQL(sql, [0])
        #             sql = "DELETE FROM coursemanagement_course WHERE CourseId = %s"
        #             executeSQL(sql, [CourseId])
        #             sql = "SET FOREIGN_KEY_CHECKS = %s"
        #             executeSQL(sql, [1])
        #
        #             return Response({"response": {"message":"Course Successfully Deleted."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
        #         else:
        #             return Response({"response": {"error":"The Instructor Doesn't Teach the Course."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        #     else:
        #         return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        #
        # else:
        #     return Response({"response": {"error":"Instructor Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ViewSet):
    ### obtain all the courses enrolled by the Student
    # 1. HTTP method: POST;
    # 2. EndPoint URL: /student/courses/
    # 3. User input: StudentId
    # 4. Response: return all the courses enrolled by the student, 200(OK)
    @action(detail=False, methods=["POST"])
    def courses(self, request):
        ID = request.data.get("StudentId", None)
        ###############################################################

        # student = Student.objects.filter(StudentId=ID).first()
        # if (student):
        #     student_courses = [] # student.Enrollments.all()
        #     enrollments = Enrollment.objects.filter(Student=student)
        #     for enrollment in enrollments:
        #         student_courses.append(Course.objects.filter(CourseId=enrollment.Course.CourseId).first())
        #
        #     serializer = CourseSerializer(student_courses, many=True) # This convert the python object list "courses" into JSON (Object to Data)
        #     student_courses = serializer.data
        #
        #     for student_course in student_courses:
        #         instructor = Instructor.objects.filter(InstructorId=student_course["Instructor"]).first()
        #         department = Department.objects.filter(DepartmentId=student_course["Department"]).first()
        #         student_course['FirstName'] = instructor.FirstName
        #         student_course['LastName'] = instructor.LastName
        #         student_course['DepartmentName'] = department.DepartmentName
        #
        #     return Response(student_courses, status=status.HTTP_200_OK)
        # else:
        #     return Response({"response": {"error":"Student Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        #################################################################################################################################

        sql = "SELECT * FROM coursemanagement_student S WHERE S.StudentId=%s"
        student = executeSQL(sql, [ID])
        if (student):
            student = student[0]

            sql = """SELECT C.*, I.FirstName, I.LastName, D.DepartmentName
                        FROM coursemanagement_student S JOIN coursemanagement_enrollment E ON (S.StudentId=E.Student_id) JOIN coursemanagement_course C ON (C.CourseId=E.Course_id) JOIN coursemanagement_instructor I ON (I.InstructorId=C.Instructor_id) JOIN coursemanagement_department D ON (D.DepartmentId=C.Department_id)
                        WHERE S.StudentId=%s"""
            student_courses = executeSQL(sql, [student["StudentId"]])
            return Response(student_courses, status=status.HTTP_200_OK)
        else:
            return Response({"response": {"error":"Student Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### enroll a course, and update the student's total credit hour and course's enrollment number
    # 1. HTTP method: PUT;
    # 2. EndPoint URL: /student/enrollCourse/
    # 3. User input: StudentId, CourseId
    # 4. Response: empty content, 202(ACCEPTED)
    @action(detail=False, methods=["POST"])
    def enrollCourse(self, request):
        StudentId = request.data.get("StudentId", None)
        CourseId = request.data.get("CourseId", None)

        student = Student.objects.filter(StudentId=StudentId).first()
        if (student):
            student_courses = [] # student.Enrollments.all()
            enrollments = Enrollment.objects.filter(Student=student)
            for enrollment in enrollments:
                student_courses.append(Course.objects.filter(CourseId=enrollment.Course.CourseId).first())

            course = Course.objects.filter(CourseId=CourseId).first()
            if (course):
                if (course in student_courses):
                    return Response({"response": {"error":"You Have Already Enrolled the Course."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if (course.Enrolled >= course.Capacity):
                        return Response({"response": {"error":"The Course Has Reached Maximum Capacity."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        student.TotalCredit += course.CreditHour
                        course.Enrolled += 1
                        # student.Enrollments.add(course)
                        newEnrollment = Enrollment(Student=student, Course=course)
                        newEnrollment.save()
                        course.save()
                        student.save()

                        return Response({"response": {"message":"Student Successfully Enrolled the Course."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"response": {"error":"Student Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### drop a course, update the student's total credit hour and course's enrollment number, and update the instructor's and course's average rating.
    # 1. HTTP method: DELETE;
    # 2. EndPoint URL: /student/dropCourse/
    # 3. User input: StudentId, CourseId
    # 4. Response: empty content, 202(ACCEPTED)
    @action(detail=False, methods=["DELETE"])
    def dropCourse(self, request):
        StudentId = request.data.get("StudentId", None)
        CourseId = request.data.get("CourseId", None)

        student = Student.objects.filter(StudentId=StudentId).first()
        if (student):
            student_courses = [] # student.Enrollments.all()
            enrollments = Enrollment.objects.filter(Student=student)
            for enrollment in enrollments:
                student_courses.append(Course.objects.filter(CourseId=enrollment.Course.CourseId).first())

            course = Course.objects.filter(CourseId=CourseId).first()
            if (course):
                if (course in student_courses):
                    student.TotalCredit -= course.CreditHour
                    course.Enrolled -= 1

                    instructor = course.Instructor
                    rating = GiveRating.objects.filter(Student=student, Course=course, Instructor=instructor).first()
                    if (rating):
                        if (course.NRating > 1):
                            course.AverageRating = float((course.AverageRating * course.NRating - rating.Rating) / (course.NRating - 1))
                            course.NRating -= 1
                        else:
                            course.NRating = 0
                            course.AverageRating = -1.0

                        if (instructor.NRating > 1):
                            instructor.AverageRating = float((instructor.AverageRating * instructor.NRating - rating.Rating) / (instructor.NRating - 1))
                            instructor.NRating -= 1
                        else:
                            instructor.NRating = 0
                            instructor.AverageRating = -1.0

                        instructor.save()
                        rating.delete()

                    # student.Enrollments.remove(course)
                    enrollment = Enrollment.objects.filter(Student=student, Course=course).first()
                    enrollment.delete()
                    student.save()
                    course.save()

                    return Response({"response": {"message":"Student Successfully Dropped the Course."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"response": {"error":"Course Not Enrolled by the Student."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"response": {"error":"Student Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    ### rate a course and its instructor, and update the associated course's AverageRating and instructor's AverageRating
    # 1. HTTP method: PUT;
    # 2. EndPoint URL: /student/giveRating/
    # 3. User input: StudentId, CourseId, Rating
    # 4. Response: empty content, 202(ACCEPTED)
    @action(detail=False, methods=["PUT"])
    def giveRating(self, request):
        #!!! Rating should be within [0, 10], reject otherwise !!!#
        StudentId = request.data.get("StudentId", None)
        CourseId = request.data.get("CourseId", None)
        Rating = request.data.get("Rating", None)

        if ((not Rating) or (not Rating.isdigit()) or (not (0 <= int(Rating) <= 10))):
            return Response({"response": {"error":"Please Enter Rating as an Integer Between 0 and 10."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        Rating = int(Rating)

        student = Student.objects.filter(StudentId=StudentId).first()
        if (not student):
            return Response({"response": {"error":"Student Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.filter(CourseId=CourseId).first()
        if (not course):
            return Response({"response": {"error":"Course Not Identified."}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        instructor = course.Instructor
        doExist = GiveRating.objects.filter(Student=student, Course=course, Instructor=instructor).first()
        if (doExist):
            return Response({"response": {"error":"You Have Already Rated the Course"}, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        newRating = GiveRating(Student=student, Course=course, Instructor=instructor, Rating=Rating)
        newRating.save()

        if (course.AverageRating == -1.0):
            course.AverageRating = float(Rating)
        else:
            course.AverageRating = float((course.AverageRating * course.NRating + Rating) / (course.NRating + 1))
        course.NRating += 1
        course.save()

        if (instructor.AverageRating == -1.0):
            instructor.AverageRating = float(Rating)
        else:
            instructor.AverageRating = float((instructor.AverageRating * instructor.NRating + Rating) / (instructor.NRating + 1))
        instructor.NRating += 1
        instructor.save()

        return Response({"response": {"message":"Rating Successfully Recorded."}, "status": 202}, status=status.HTTP_202_ACCEPTED)
