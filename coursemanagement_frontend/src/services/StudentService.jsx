import axios from '../axios';

export const StudentService = {
    getAllStudents: function(searchStudentInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        // Endpoint URL: /students/;
        const searchStudentRequest = {
            searchDepartmentNames: searchStudentInfo.searchDepartments,
        };

        return axios.post('/students/', searchStudentRequest);
    },

    getCourseStudents: function(searchCourseStudentInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        // Endpoint URL: /instructor/students/;
        const searchCourseStudentRequest = {
            InstructorId: searchCourseStudentInfo.instructorId,
            CourseId: searchCourseStudentInfo.courseId,
        };

        return axios.post('/instructor/students/', searchCourseStudentRequest); // This is XHR, which returns a promise, with either success with the full courses list as "response" or failure with an error "error"
    },
}
