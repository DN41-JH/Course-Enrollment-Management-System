import React, { useState, useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import StudentTable from '../components/tables/StudentTable';
import { StudentService } from '../services/StudentService';
// import cookie from 'react-cookies';
// import { JWT_TOKEN_COOKIE_NAME } from '../constants';

// This is the "AllCourses" [view] that is designed to render the course table that contains the all_courses_data.

export default function AllInstructors() {
    // 1. call backend API to get data, via XHR (XML-Http-Request)
    // 2. refresh the data state and trigger re-render
    // ===> Must be within 'useEffect'

    // const token = cookie.load(JWT_TOKEN_COOKIE_NAME);

    // student searching input
    const [searchDepartments, setSearchDepartments] = useState(null);

    // students
    const [allStudents, setAllStudents] = useState([]); // The all_instructors_data for render is set as the state

    useEffect(() => {
        getAllStudents();
    });
    
    function getAllStudents() {
        const searchStudentInfo = {
            searchDepartments: searchDepartments,
        };

        // Pull data via XHR ===> Must be called within 'useEffect'
        StudentService.getAllStudents(searchStudentInfo)
            .then((response) => {
                setAllStudents(response.data);
            })
            .catch((error) => console.log(error));
    }

    function renderSearchFields() {
        return (
            <div>
                <TextField
                    margin="dense"
                    id="searchDepartments"
                    label="Search Students Who Belong to Certain Departments or Who Enroll Courses of Certain Departments, Enter Target Departments Separated by Commas (i.e. 'CS,PHYS,ECE')"
                    type="username"
                    fullWidth
                    onChange={(event) => setSearchDepartments(event.target.value)}
                />
            </div>
        );
    }

    return (
        <div>
            {renderSearchFields()}

            <StudentTable 
                students={allStudents}
            />
        </div>
    );
};