import axios from "../axios";

export const UserService = {
    checkStatus: function(checkStatusInfo) {
        const checkStatusRequest = {
            ID: checkStatusInfo.Id,
            Role: checkStatusInfo.Role,
        }

        // (Must follow the EndPoint URL as specified in the backend url pattern)
        return axios.post('/checkStatus/', checkStatusRequest);
    },

    register: function(registerInfo) {
        const registerRequest = {
            UserName: registerInfo.username,
            PassWord: registerInfo.password,
            FirstName: registerInfo.firstname,
            LastName: registerInfo.lastname,
            Email: registerInfo.email,
            Role: registerInfo.role,
            DepartmentName: registerInfo.department,
        };

        // (Must follow the EndPoint URL as specified in the backend url pattern)
        return axios.post('/register/', registerRequest); // This is XHR, which returns a promise, with either success with the desired token as "response" or failure with an error "error"
    },

    login: function(loginInfo) {
        const loginRequest = {
            UserName: loginInfo.username,
            PassWord: loginInfo.password,
        };

        // (Must follow the EndPoint URL as specified in the backend url pattern)
        return axios.post('/login/', loginRequest); // This is XHR, which returns a promise, with either success with the desired token as "response" or failure with an error "error"
    },

    withdraw: function(withdrawInfo) {
        const withdrawRequest = {
            data: {
                ID: withdrawInfo.Id,
                Role: withdrawInfo.Role,
            },
        };

        // (Must follow the EndPoint URL as specified in the backend url pattern)
        return axios.delete('/withdraw/', withdrawRequest); // This is XHR, which returns a promise, with either success with the desired token as "response" or failure with an error "error"
    },
}