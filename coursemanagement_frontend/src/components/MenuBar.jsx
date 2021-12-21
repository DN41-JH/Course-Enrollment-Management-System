// This Navigation Menu Bar component is copied from CSS template from material-UI: “https://material-ui.com/components/app-bar/”

import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom';
import LoginDialog from './dialogs/LoginDialog';
import SignUpDialog from './dialogs/SignUpDialog';
import WithdrawDialog from './dialogs/WithdrawDialog';
import NewCourseDialog from './dialogs/NewCourseDialog';
import StatusDialog from './dialogs/StatusDialog';
// import cookie from 'react-cookies';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

export default function MenuBar() {
  const classes = useStyles();

  const [openStatusDialog, setOpenStatusDialog] = useState(false);
  const [openLoginDialog, setOpenLoginDialog] = useState(false);
  const [openSignUpDialog, setOpenSignUpDialog] = useState(false);
  const [openWithdrawDialog, setOpenWithdrawDialog] = useState(false);
  const [openNewCourseDialog, setOpenNewCourseDialog] = useState(false);

  const [errorMessage_LoginDialog, setErrorMessage_LoginDialog] = useState("");
  const [errorMessage_SignUpDialog, setErrorMessage_SignUpDialog] = useState("");
  const [errorMessage_WithdrawDialog, setErrorMessage_WithdrawDialog] = useState("");
  const [errorMessage_NewCourseDialog, setErrorMessage_NewCourseDialog] = useState("");

  // const isLoggedIn = cookie.load(JWT_TOKEN_COOKIE_NAME) ? true : false;
  const isLoggedIn = (window.sessionStorage.getItem("Id") && window.sessionStorage.getItem("Role")) ? true : false;

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            Course Management System
          </Typography>

          {renderStatus()}
          <Button color="inherit" component={Link} to="/department_ratings"> All Departments </Button>
          <Button color="inherit" component={Link} to="/courses"> All Courses </Button>
          <Button color="inherit" component={Link} to="/instructors"> All Instructors </Button>
          <Button color="inherit" component={Link} to="/students"> All Students </Button>
          {renderMyCourses()}
          {renderAddNewCourse()}
          {/* "component" and "to" attributes are to enable the material-UI component with desired react-router-dom functionality */}
          <Button color="inherit" onClick={handleLoginButtonClick}> {isLoggedIn ? "Logout" : "Login"} </Button>
          <Button color="inherit" onClick={handleSignUpButtonClick}> {isLoggedIn ? "Withdraw" : "Sign Up"} </Button>
        </Toolbar>
      </AppBar>

      <StatusDialog
        open={openStatusDialog}
        onClose={handleStatusDialogClose}
      />
      
      <LoginDialog
        open={openLoginDialog}
        errorMessage={errorMessage_LoginDialog}
        onErrorMessageChange={handleLoginDialogErrorMessageUpdate}
        onClose={handleLoginDialogClose}
      />
      <SignUpDialog
        open={openSignUpDialog}
        errorMessage={errorMessage_SignUpDialog}
        onErrorMessageChange={handleSignUpDialogErrorMessageUpdate}
        onClose={handleSignUpDialogClose}
      />
      <WithdrawDialog
        open={openWithdrawDialog}
        errorMessage={errorMessage_WithdrawDialog}
        onErrorMessageChange={handleWithdrawDialogErrorMessageUpdate}
        onClose={handleWithdrawDialogClose}
      />
      <NewCourseDialog
        open={openNewCourseDialog}
        errorMessage={errorMessage_NewCourseDialog}
        onErrorMessageChange={handleNewCourseDialogErrorMessageUpdate}
        onClose={handleNewCourseDialogClose}
      />
    </div>
  );

  function renderStatus() {
    return <Button color="inherit" onClick={handleCheckStatusButtonClick}> My Status </Button>; 
  }

  function renderMyCourses() {
      if (isLoggedIn) {
        return <Button color="inherit" component={Link} to="/user_courses"> My Courses </Button>;
      }
  }

  function renderAddNewCourse() {
      if (isLoggedIn && (window.sessionStorage.getItem("Role") === "Instructor")) {
        return <Button color="inherit" onClick={handleAddNewCourseButtonClick}> ADD NEW COURSE </Button>;
      }
  }

  function handleCheckStatusButtonClick() {
      setOpenStatusDialog(true);
  }

  function handleSignUpButtonClick() {
      if (isLoggedIn) {
        setOpenWithdrawDialog(true);
      } else {
        setOpenSignUpDialog(true);
      }
  }
  
  function handleLoginButtonClick() {
    if (isLoggedIn) {
      // cookie.remove(JWT_TOKEN_COOKIE_NAME);
      window.sessionStorage.removeItem("Id");
      window.sessionStorage.removeItem("Role");
      window.location.reload();
    } else {
      // open the login dialog form when login
      setOpenLoginDialog(true);
    }
  }

  function handleAddNewCourseButtonClick() {
    setOpenNewCourseDialog(true);
  }

  function handleNewCourseDialogErrorMessageUpdate(errorMessage) {
    setErrorMessage_NewCourseDialog(errorMessage);
  }

  function handleSignUpDialogErrorMessageUpdate(errorMessage) {
    setErrorMessage_SignUpDialog(errorMessage);
  }

  function handleLoginDialogErrorMessageUpdate(errorMessage) {
    setErrorMessage_LoginDialog(errorMessage);
  }

  function handleWithdrawDialogErrorMessageUpdate(errorMessage) {
    setErrorMessage_WithdrawDialog(errorMessage);
  }

  function handleStatusDialogClose() {
    setOpenStatusDialog(false);
  }

  function handleSignUpDialogClose() {
    setOpenSignUpDialog(false);
    setErrorMessage_SignUpDialog("");
  }

  function handleLoginDialogClose() {
    setOpenLoginDialog(false);
    setErrorMessage_LoginDialog("");
  }

  function handleWithdrawDialogClose() {
    setOpenWithdrawDialog(false);
    setErrorMessage_WithdrawDialog("");
  }

  function handleNewCourseDialogClose() {
    setOpenNewCourseDialog(false);
    setErrorMessage_NewCourseDialog("");
  }
}