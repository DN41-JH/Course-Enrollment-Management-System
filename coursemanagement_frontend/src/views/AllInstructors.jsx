import React, { useState, useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import InstructorTable from '../components/tables/InstructorTable';
import { InstructorService } from '../services/InstructorService';
// import cookie from 'react-cookies';
// import { JWT_TOKEN_COOKIE_NAME } from '../constants';

// This is the "AllCourses" [view] that is designed to render the course table that contains the all_courses_data.

export default function AllInstructors() {
    // 1. call backend API to get data, via XHR (XML-Http-Request)
    // 2. refresh the data state and trigger re-render
    // ===> Must be within 'useEffect'

    // const token = cookie.load(JWT_TOKEN_COOKIE_NAME);

    // instructor searching input
    const [searchFirstName, setSearchFirstName] = useState(null);
    const [searchLastName, setSearchLastName] = useState(null);
    const [searchDepartment, setSearchDepartment] = useState(null);

    // instructors
    const [allInstructors, setAllInstructors] = useState([]); // The all_instructors_data for render is set as the state

    useEffect(() => {
        getAllInstructors();
    });
    
    function getAllInstructors() {
        const searchInstructorInfo = {
            searchFirstName: searchFirstName,
            searchLastName: searchLastName,
            searchDepartment: searchDepartment,
        };

        // Pull data via XHR ===> Must be called within 'useEffect'
        InstructorService.getAllInstructors(searchInstructorInfo)
            .then((response) => {
                setAllInstructors(response.data);
            })
            .catch((error) => console.log(error));
    }

    function renderSearchFields() {
        return (
            <div>
                <TextField
                    margin="dense"
                    id="searchFirstName"
                    label="Search Instructor's First Name"
                    type="username"
                    // fullWidth
                    style = {{width: 300}}
                    onChange={(event) => setSearchFirstName(event.target.value)}
                />
                <span> </span>
                <TextField
                    margin="dense"
                    id="searchLastName"
                    label="Search Instructor's Last Name"
                    type="username"
                    // fullWidth
                    style = {{width: 300}}
                    onChange={(event) => setSearchLastName(event.target.value)}
                />
                <span> </span>
                <TextField
                    margin="dense"
                    id="searchDepartment"
                    label="Search Instructor's Department"
                    type="username"
                    // fullWidth
                    style = {{width: 300}}
                    onChange={(event) => setSearchDepartment(event.target.value)}
                />
            </div>
        );
    }

    return (
        <div>
            {renderSearchFields()}

            <InstructorTable 
                instructors={allInstructors}
            />
        </div>
    );
};