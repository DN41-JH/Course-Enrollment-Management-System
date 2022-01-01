import React from "react";
import './Bootstrap.css';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import MenuBar from "./components/MenuBar";
import Footer from "./components/Footer";
import UserCourses from "./views/UserCourses";
import AllDepartments from "./views/AllDepartments";
import AllStudents from "./views/AllStudents";
import AllCourses from "./views/AllCourses";
import AllInstructors from "./views/AllInstructors";

export default function App() {
  return (
    // This webpage-routing-supported App is copied from "react-router-dom": https://reactrouter.com/web/example/basic.
    // The purpose of <Router> <Router /> is to realize the webpage routing functionality.
    // The purpose of <Switch> <Switch /> is to render certain desired [view] when webpage routing is triggered.

    // <MenuBar />: The newly created navigation bar [component] that contains buttons for user to trigger certain routing.
    // <AllCourses /> : The newly created [view] that is designed to render the course table component that contains the all courses data.
    // <EnrolledCourses /> : The newly create [view] that is designed to render the course table component that contains the enroled courses data.
    // <Login /> : The newly created [view] that is designed to render the ............

    
    <Router>
      <div>
        {/* <ul>
          <li>
            <Link to="/"> All Courses </Link>
          </li>
          <li>
            <Link to="/enrolled_courses"> Enrolled Courses </Link>
          </li>
          <li>
            <Link to="/login"> login </Link>
          </li>
        </ul> */}
  
        <MenuBar />

        <hr />

        {/*
          A <Switch> looks through all its children <Route> elements and renders the first one whose path
          matches the current URL. Use a <Switch> any time you have multiple routes, but you want only one
          of them to render at a time.
        */}
        <Switch>
          <Route exact path="/department_ratings">
            <AllDepartments />
          </Route>

          <Route exact path="/students">
            <AllStudents />
          </Route>

          <Route exact path="/courses">
            <AllCourses />
          </Route>

          <Route exact path="/instructors">
            <AllInstructors />
          </Route>

          <Route path="/user_courses/">
            <UserCourses />
          </Route>
        </Switch>
      </div>

      <Footer />
    </Router>
  );
}