import React from 'react';
import CourseTable from '../components/tables/CourseTable';
// import { JWT_TOKEN_COOKIE_NAME } from '../constants';
import { CourseService } from '../services/CourseService';
import { StudentService } from '../services/StudentService';
// import cookie from "react-cookies";
import ActionAlert from '../components/alerts/ActionAlert';
import RateCourseDialog from '../components/dialogs/RateCourseDialog';
import EditCourseDialog from '../components/dialogs/EditCourseDialog';
import ViewCourseStudentsDialog from '../components/dialogs/ViewCourseStudentsDialog';

// This is the "UserCourses" [view] that is designed to render the course table that contains the enrolled_courses_data.
  
export default class UserCourses extends React.Component {
    // 1. call backend API to get data, via XHR (XML-Http-Request)
    // 2. refresh the data state and trigger re-render
    // ===> Must be within 'componentDidMount'

    constructor(props) {
        super(props);
        this.state = {
            userRole: null,
            userCourses: [],

            openRateCourseDialog: false,
            rateCourse: null,
            errorMessage_RateCourseDialog: "",

            openEditCourseDialog: false,
            editCourse: null,
            errorMessage_EditCourseDialog: "",

            openViewCourseStudentsDialog: false,
            courseStudents: [],

            alertSeverity: "",
            alertMessage: "",
            alertOpen: false,
        };

        // Bind all the callback functions
        this.handleDropCourse = this.handleDropCourse.bind(this);
        this.handleRateCourse = this.handleRateCourse.bind(this);

        this.handleEditCourse = this.handleEditCourse.bind(this);
        this.handleViewCourseStudents = this.handleViewCourseStudents.bind(this);
        this.handleDeleteCourse = this.handleDeleteCourse.bind(this);

        this.handleAlertClick = this.handleAlertClick.bind(this);

        this.handleRateCourseDialogErrorMessageUpdate = this.handleRateCourseDialogErrorMessageUpdate.bind(this);
        this.handleRateCourseDialogClose = this.handleRateCourseDialogClose.bind(this);

        this.handleEditCourseDialogErrorMessageUpdate = this.handleEditCourseDialogErrorMessageUpdate.bind(this);
        this.handleEditCourseDialogClose = this.handleEditCourseDialogClose.bind(this);

        this.handleViewCourseStudentsDialogClose = this.handleViewCourseStudentsDialogClose.bind(this);
    }

    componentDidMount() {
        this.getUserCourses();
    }

    getUserCourses() {
        // Pull data via XHR
        // This must be called within "componentDidMount"
        const userInfo = {
            Id: window.sessionStorage.getItem("Id") ? parseInt(window.sessionStorage.getItem("Id")) : 0,
            Role: window.sessionStorage.getItem("Role") ? window.sessionStorage.getItem("Role") : "Unknown",
        };

        CourseService.getUserCourses(userInfo)
            .then((response) => {
                this.setState(
                    {
                        userCourses: response.data,
                        userRole: window.sessionStorage.getItem("Role"),
                    });
            }) // re-render by updating the state
            .catch((error) => console.log(error));
    }

    handleDropCourse(course) {
        // const token = cookie.load(JWT_TOKEN_COOKIE_NAME);
        const dropCourseInfo = {
            studentId: parseInt(window.sessionStorage.getItem("Id")),
            courseId: course.CourseId,
        };

        CourseService.dropCourse(dropCourseInfo)
            .then((response) => {
                this.setState({
                    alertSeverity: "success",
                    alertMessage: `Successfully dropped Course ${course.Number}`,
                    alertOpen: true,
                });

                this.getUserCourses();
            })
            .catch((error) => {
                // alert(`Failed to withdraw Course ${course.course_name}`);
                this.setState({
                    alertSeverity: "error",
                    alertMessage: `${error.response.data.response.error}`,
                    alertOpen: true,
                });
            });
    }

    handleRateCourse(course) {
        this.setState({
            openRateCourseDialog: true,
            rateCourse: course,
        });
    }

    handleEditCourse(course) {
        this.setState({
            openEditCourseDialog: true,
            editCourse: course,
        });
    }

    handleViewCourseStudents(course) {
        const searchCourseStudentInfo = {
            instructorId: parseInt(window.sessionStorage.getItem("Id")),
            courseId: course.CourseId,
        }

        StudentService.getCourseStudents(searchCourseStudentInfo)
            .then((response) => {
                this.setState({
                    courseStudents: response.data,
                    openViewCourseStudentsDialog: true,
                });
            })
            .catch((error) => {
                this.setState({
                    alertSeverity: "error",
                    alertMessage: `${error.response.data.response.error}`,
                    alertOpen: true,
                });
            });
    }

    handleDeleteCourse(course) {
        // const token = cookie.load(JWT_TOKEN_COOKIE_NAME);
        const deleteCourseInfo = {
            instructorId: parseInt(window.sessionStorage.getItem("Id")),
            courseId: course.CourseId,
        };

        CourseService.deleteCourse(deleteCourseInfo)
            .then((response) => {
                this.setState({
                    alertSeverity: "success",
                    alertMessage: `Successfully deleted Course ${course.Number}`,
                    alertOpen: true,
                });

                this.getUserCourses();
            })
            .catch((error) => {
                // alert(`Failed to withdraw Course ${course.course_name}`);
                this.setState({
                    alertSeverity: "error",
                    alertMessage: `${error.response.data.response.error}`,
                    alertOpen: true,
                });
            });
    }

    handleRateCourseDialogErrorMessageUpdate(errorMessage) {
        this.setState({
            errorMessage_RateCourseDialog: errorMessage,
        });
    }

    handleRateCourseDialogClose() {
        this.setState({
            openRateCourseDialog: false,
            rateCourse: null,
            errorMessage_RateCourseDialog: "",
        });
    }

    handleEditCourseDialogErrorMessageUpdate(errorMessage) {
        this.setState({
            errorMessage_EditCourseDialog: errorMessage,
        });
    }

    handleEditCourseDialogClose() {
        this.setState({
            openEditCourseDialog: false,
            editCourse: null,
            errorMessage_EditCourseDialog: "",
        });
    }

    handleViewCourseStudentsDialogClose() {
        this.setState({
            openViewCourseStudentsDialog: false,
            courseStudents: [],
        });
    }

    handleAlertClick() {
        this.setState({
            alertOpen: false,
        });
    }

    render() {
        return (
            <div>
                <ActionAlert 
                    alertSeverity={this.state.alertSeverity} 
                    alertMessage={this.state.alertMessage}
                    open={this.state.alertOpen}
                    onAlertClick={this.handleAlertClick}
                />

                <CourseTable
                    courses={this.state.userCourses}
                    allCourseView={false}
                    role={this.state.userRole}
                    onActionButtonClick_Drop={this.handleDropCourse}
                    onActionButtonClick_Rate={this.handleRateCourse}
                    onActionButtonClick_Edit={this.handleEditCourse}
                    onActionButtonClick_Delete={this.handleDeleteCourse}
                    onActionButtonClick_ViewStudents={this.handleViewCourseStudents}
                />

                <RateCourseDialog
                    open={this.state.openRateCourseDialog}
                    course={this.state.rateCourse}
                    errorMessage={this.state.errorMessage_RateCourseDialog}
                    onErrorMessageChange={this.handleRateCourseDialogErrorMessageUpdate}
                    onClose={this.handleRateCourseDialogClose}
                />

                <EditCourseDialog
                    open={this.state.openEditCourseDialog}
                    course={this.state.editCourse}
                    errorMessage={this.state.errorMessage_EditCourseDialog}
                    onErrorMessageChange={this.handleEditCourseDialogErrorMessageUpdate}
                    onClose={this.handleEditCourseDialogClose}
                />

                <ViewCourseStudentsDialog
                    open={this.state.openViewCourseStudentsDialog}
                    courseStudents={this.state.courseStudents}
                    onClose={this.handleViewCourseStudentsDialogClose}
                />
            </div>
        );        
    }

};

// Data extract procedure (2021.5.9) ===>
//  1. Make connection between the data repository and the React framework (via axios)
//  2. Define the data service (as an object), which contains function(s) that asks the data repository for certain data (via XHR)
//  [3. Call the desired data service function to extract the desired data]