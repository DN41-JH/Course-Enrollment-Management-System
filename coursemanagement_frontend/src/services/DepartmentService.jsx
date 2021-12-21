import axios from '../axios';

export const DepartmentService = {
    getAllDepartments: function() {
        // (Must refer to the corresponding backend API)
        // HTTP Method: GET;
        // Endpoint URL: /departmentsRating;

        return (
            axios.get('/departmentsRating/') // This is XHR, which returns a promise, with either success with the full courses list as "response" or failure with an error "error"
        );
    },
}
