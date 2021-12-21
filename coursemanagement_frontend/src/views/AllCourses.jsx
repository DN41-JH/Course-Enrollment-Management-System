import React, { useState, useEffect } from 'react';
import CourseTable from '../components/tables/CourseTable';
import TextField from '@material-ui/core/TextField';
import { CourseService } from '../services/CourseService';
// import cookie from 'react-cookies';
// import { JWT_TOKEN_COOKIE_NAME } from '../constants';
import ActionAlert from '../components/alerts/ActionAlert';

// This is the "AllCourses" [view] that is designed to render the course table that contains the all_courses_data.

export default function AllCourses() {
    // 1. call backend API to get data, via XHR (XML-Http-Request)
    // 2. refresh the data state and trigger re-render
    // ===> Must be within 'useEffect'

    // const token = cookie.load(JWT_TOKEN_COOKIE_NAME);

    // courses
    const [allCourses, setAllCourses] = useState([]); // The all_courses_data for render is set as the state

    // authentication status
    const [userRole, setUserRole] = useState(null);

    // course searching input
    const [searchCourseNumber, setSearchCourseNumber] = useState(null);
    const [searchFirstName, setSearchFirstName] = useState(null);
    const [searchLastName, setSearchLastName] = useState(null);

    // alerts
    const [alertOpen, setAlertOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertSeverity, setAlertSeverity] = useState("");

    useEffect(() => {
        getAllCourses();
    });
    
    function getAllCourses() {
        const searchCourseInfo = {
            searchCourseNumber: searchCourseNumber,
            searchFirstName: searchFirstName,
            searchLastName: searchLastName,
        };

        // Pull data via XHR ===> Must be called within 'useEffect'
        CourseService.getAllCourses(searchCourseInfo)
            .then((response) => {
                setAllCourses(response.data);
                // setIsLoggedIn(token ? true : false);
                setUserRole(window.sessionStorage.getItem("Role"));
            })
            .catch((error) => console.log(error));
    }

    function handleEnrollCourse(course) {
        const enrollInfo = {
            studentId: parseInt(window.sessionStorage.getItem("Id")),
            courseId: course.CourseId
        }

        CourseService.enrollCourse(enrollInfo)
            .then((response) => {
                // alert(`Successfully enrolled Course ${course.course_name}`)
                setAlertOpen(true);
                setAlertMessage(`Successfully enrolled Course ${course.Title}`);
                setAlertSeverity("success");
            })
            .catch((error) => {
                // alert(`Failed to enroll Course ${course.course_name}`)
                setAlertOpen(true);
                setAlertMessage(`${error.response.data.response.error}`);
                setAlertSeverity("error");
            }
        );
    }

    function renderSearchFields() {
        return (
            <div>
                <TextField
                    margin="dense"
                    id="courseNumber"
                    label="Search Course Number"
                    type="username"
                    // fullWidth
                    style = {{width: 300}}
                    onChange={(event) => setSearchCourseNumber(event.target.value)}
                />
                <span> </span>
                <TextField
                    margin="dense"
                    id="courseNumber"
                    label="Search Instructor First Name"
                    type="username"
                    // fullWidth
                    style = {{width: 300}}
                    onChange={(event) => setSearchFirstName(event.target.value)}
                />
                <span> </span>
                <TextField
                    margin="dense"
                    id="courseNumber"
                    label="Search Instructor Last Name"
                    type="username"
                    // fullWidth
                    style = {{width: 300}}
                    onChange={(event) => setSearchLastName(event.target.value)}
                />
            </div>
        );
    }
    
    function handleAlertClick() {
        setAlertOpen(false);
    }

    return (
        <div>
            <ActionAlert 
                alertSeverity={alertSeverity} 
                alertMessage={alertMessage}
                open={alertOpen}
                onAlertClick={handleAlertClick}
            />

            {renderSearchFields()}

            <CourseTable 
                courses={allCourses} 
                // actionButtonLabel={token ? "Enroll" : null}
                allCourseView={true}
                role={userRole}
                onActionButtonClick_Enroll={handleEnrollCourse}
            />
        </div>
    );
};


// Data extract procedure (2021.5.9) ===>
//  1. Make connection between the data repository and the React framework (via axios)
//  2. Define the data service (as an object), which contains function(s) that asks the data repository for certain data (via XHR)
//  [3. Call the desired data service function to extract the desired data via XHR]