import axios from '../axios';

export const CourseService = {
    getAllCourses: function(searchCourseInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        // Endpoint URL: /courses/;
        const searchCourseRequest = {
            searchCourseNumber: searchCourseInfo.searchCourseNumber,
            searchInstructorFirstName: searchCourseInfo.searchFirstName,
            searchInstructorLastName: searchCourseInfo.searchLastName,
        };

        return (
            axios.post('/courses/', searchCourseRequest) // This is XHR, which returns a promise, with either success with the full courses list as "response" or failure with an error "error"
        );
    },

    getUserCourses: function(userInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        let getUserCoursesRequest = {};
        let URL = "";

        if (userInfo.Role === "Instructor") {
            // EndPoint URL: /instructor/courses/
            URL = '/instructor/courses/';
            getUserCoursesRequest.InstructorId = userInfo.Id;
        } else if (userInfo.Role === "Student") {
            // EndPoint URL: /student/courses/
            URL = '/student/courses/';
            getUserCoursesRequest.StudentId = userInfo.Id;
        }
        
        return axios.post(URL, getUserCoursesRequest);
    },

    createCourse: function(newCourseInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        // EndPoint URL: /instructor/createCourse/
        const createCourseRequest = {
            Number: newCourseInfo.number,
            Title: newCourseInfo.title,
            Section: newCourseInfo.section,
            Type: newCourseInfo.type,
            CreditHour: newCourseInfo.creditHour,
            StartTime: newCourseInfo.startTime,
            EndTime: newCourseInfo.endTime,
            DaysOfWeek: newCourseInfo.daysOfWeek,
            Room: newCourseInfo.room,
            Building: newCourseInfo.building,
            Capacity: newCourseInfo.capacity,
            InstructorId: newCourseInfo.instructorId,
        };

        return axios.post('/instructor/createCourse/', createCourseRequest);
    },

    editCourse: function(editCourseInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: PUT;
        // EndPoint URL: /instructor/updateCourse/
        const editCourseRequest = {
            CourseId: editCourseInfo.courseId,
            InstructorId: editCourseInfo.instrucotrId,
            TargetField: editCourseInfo.targetField,
            NewContent: editCourseInfo.newContent,
        };

        return axios.put('/instructor/updateCourse/', editCourseRequest);
    },

    deleteCourse: function(deleteCourseInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: DELETE;
        // EndPoint URL: /instructor/deleteCourse/
        const deleteCourseRequest = {
            data: {
                InstructorId: deleteCourseInfo.instructorId,
                CourseId: deleteCourseInfo.courseId,
            },
        };

        return axios.delete('/instructor/deleteCourse/', deleteCourseRequest);
    },

    enrollCourse: function(enrollInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        // EndPoint URL: /student/enrollCourse/; 
        const enrollRequest = {
            StudentId: enrollInfo.studentId,
            CourseId: enrollInfo.courseId,
        };

        return axios.post('/student/enrollCourse/', enrollRequest);
    },

    dropCourse: function(dropCourseInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: DELETE;
        // EndPoint URL: /student/dropCourse/
        const dropCourseRequest = {
            data: {
                StudentId: dropCourseInfo.studentId,
                CourseId: dropCourseInfo.courseId,
            },
        }

        return axios.delete('/student/dropCourse/', dropCourseRequest);
    },

    rateCourse: function(rateCourseInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: PUT;
        // EndPoint URL: /student/giveRating/
        const rateCourseRequest = {
            StudentId: rateCourseInfo.studentId,
            CourseId: rateCourseInfo.courseId,
            Rating: rateCourseInfo.rating,
        };

        return axios.put('/student/giveRating/', rateCourseRequest);
    },
}

// Data extract procedure (2021.5.9) ===>
//  1. Make connection between the data repository and the React framework (via axios)
//  [2. Define the data service (as an object), which contains function(s) that asks the data repository for certain data (via XHR)]
//  3. Call the desired data service function to extract the desired data