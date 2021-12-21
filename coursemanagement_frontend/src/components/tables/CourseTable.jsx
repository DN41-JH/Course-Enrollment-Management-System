// This CourseTable component is copied from CSS template from material-UI: “https://material-ui.com/components/tables/”

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Button } from '@material-ui/core';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

export default function CourseTable(props) {
  const classes = useStyles();

  function renderActionButton(item) {
    if (props.allCourseView) {
      if (props.role === "Student") {
        return (
          <TableCell align="right"> 
            <Button color="primary" variant="contained" onClick={() => props.onActionButtonClick_Enroll(item)}> Enroll </Button>
          </TableCell>
        );
      } else {
        return null;
      }
    } else {
      if (props.role === "Student") {
        return (
          <TableCell align="right">
            <Button color="primary" variant="contained" onClick={() => props.onActionButtonClick_Rate(item)}> Rate </Button>
            <Button color="warning" variant="contained" onClick={() => props.onActionButtonClick_Drop(item)}> Drop </Button>
          </TableCell>
        );
      } else if (props.role === "Instructor") {
        return (
          <TableCell align="right">
            <Button color="primary" variant="contained" onClick={() => props.onActionButtonClick_Edit(item)}> Edit </Button>
            <Button color="secondary" variant="contained" onClick={() => props.onActionButtonClick_Delete(item)}> Delete </Button>
            <Button color='default' variant="contained" onClick={() => props.onActionButtonClick_ViewStudents(item)}> View Students </Button>
          </TableCell>
        );
      } else {
        return null;
      }
    }
  }

  function renderCourses() {
    return (
        props.courses.map((item, i) => (
            <TableRow key={item.CourseId}>
              <TableCell component="th" scope="row"> {i + 1} </TableCell>
              <TableCell align="right"> {item.Number} </TableCell>
              <TableCell align="right"> {item.Title} </TableCell>
              <TableCell align="right"> {item.Section} </TableCell>
              <TableCell align="right"> {item.Type} </TableCell>
              <TableCell align="right"> {item.CreditHour} </TableCell>
              <TableCell align="right"> {item.StartTime} </TableCell>
              <TableCell align="right"> {item.EndTime} </TableCell>
              <TableCell align="right"> {item.DaysOfWeek} </TableCell>
              <TableCell align="right"> {item.Room} </TableCell>
              <TableCell align="right"> {item.Building} </TableCell>
              <TableCell align="right"> {item.Capacity} </TableCell>
              <TableCell align="right"> {item.Enrolled} </TableCell>
              <TableCell align="right"> {(item.AverageRating < 0) ? "No Ratings" : item.AverageRating} </TableCell>
              <TableCell align="right"> {item.FirstName + ' ' + item.LastName} </TableCell>
              <TableCell align="right"> {item.DepartmentName} </TableCell>
              {renderActionButton(item)}
            </TableRow>
          ))
    );
  }

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell> # </TableCell>
            <TableCell align="right"> Course </TableCell>
            <TableCell align="right"> Title </TableCell>
            <TableCell align="right"> Section </TableCell>
            <TableCell align="right"> Type </TableCell>
            <TableCell align="right"> Credit Hour </TableCell>
            <TableCell align="right"> Start Time </TableCell>
            <TableCell align="right"> End Time </TableCell>
            <TableCell align="right"> Days </TableCell>
            <TableCell align="right"> Room </TableCell>
            <TableCell align="right"> Building </TableCell>
            <TableCell align="right"> Capacity </TableCell>
            <TableCell align="right"> Enrolled </TableCell>
            <TableCell align="right"> Average Rating </TableCell>
            <TableCell align="right"> Instructor </TableCell>
            <TableCell align="right"> Department </TableCell>
            {(!props.allCourseView || props.role === "Student") ? <TableCell align="right"> Action </TableCell> : null}
          </TableRow>
        </TableHead>

        <TableBody>
          {renderCourses()}
        </TableBody>
      </Table>
    </TableContainer>
  );
}