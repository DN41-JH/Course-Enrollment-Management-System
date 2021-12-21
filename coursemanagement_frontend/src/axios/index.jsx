import axios from 'axios';

export default axios.create({
    // baseURL: "https://37f5601c-9df2-44f1-932c-733b4b5b9a4c.mock.pstmn.io",

    // Local base URL
    baseURL: "http://127.0.0.1:8000/"

    // Cluster base URL
    // baseURL: "http://a118422103fea4a6a80a26246316412e-2039132936.us-west-2.elb.amazonaws.com:8000"
});


// Data extract procedure (2021.5.9) ===>
//  [1. Make connection between the data repository and the React framework (via axios)]
//  2. Define the data service (as an object), which contains function(s) that asks the data repository for certain data (via XHR)
//  3. Call the desired data service function to extract the desired data