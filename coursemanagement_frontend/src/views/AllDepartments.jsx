import React, { useState, useEffect } from 'react';
import DepartmentTable from '../components/tables/DepartmentTable';
import { DepartmentService } from '../services/DepartmentService';
// import cookie from 'react-cookies';
// import { JWT_TOKEN_COOKIE_NAME } from '../constants';

// This is the "AllCourses" [view] that is designed to render the course table that contains the all_courses_data.

export default function AllDepartments() {
    // 1. call backend API to get data, via XHR (XML-Http-Request)
    // 2. refresh the data state and trigger re-render
    // ===> Must be within 'useEffect'

    // const token = cookie.load(JWT_TOKEN_COOKIE_NAME);

    // departments
    const [allDepartments, setAllDepartments] = useState([]); // The all_departments_data for render is set as the state

    useEffect(() => {
        getAllDepartments();
    });
    
    function getAllDepartments() {
        // Pull data via XHR ===> Must be called within 'useEffect'
        DepartmentService.getAllDepartments()
            .then((response) => {
                setAllDepartments(response.data);
            })
            .catch((error) => console.log(error));
    }

    return (
        <div>
            <DepartmentTable
                departments={allDepartments}
            />
        </div>
    );
};