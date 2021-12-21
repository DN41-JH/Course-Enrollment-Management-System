import axios from '../axios';

export const InstructorService = {
    getAllInstructors: function(searchInstructorInfo) {
        // (Must refer to the corresponding backend API)
        // HTTP Method: POST;
        // Endpoint URL: /instructors/;
        const searchInstructorRequest = {
            searchInstructorFirstName: searchInstructorInfo.searchFirstName,
            searchInstructorLastName: searchInstructorInfo.searchLastName,
            searchInstructorDepartment: searchInstructorInfo.searchDepartment,
        };

        return (
            axios.post('/instructors/', searchInstructorRequest) // This is XHR, which returns a promise, with either success with the full courses list as "response" or failure with an error "error"
        );
    },
}
