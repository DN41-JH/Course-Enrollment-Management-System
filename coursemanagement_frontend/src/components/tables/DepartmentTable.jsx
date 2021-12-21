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

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

export default function InstructorTable(props) {
  const classes = useStyles();

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell> # </TableCell>
            <TableCell align="right"> Department Name </TableCell>
            <TableCell align="right"> Course Ratings Received </TableCell>
            <TableCell align="right"> Average Rating </TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {renderDepartments()}
        </TableBody>
      </Table>
    </TableContainer>
  );

  function renderDepartments() {
    return (
        props.departments.map((item, i) => (
            <TableRow key={item.InstructorId}>
              <TableCell component="th" scope="row"> {i + 1} </TableCell>
              <TableCell align="right"> {item.DepartmentName} </TableCell>
              <TableCell align="right"> {item.NRating ? item.NRating : 0} </TableCell>
              <TableCell align="right"> {(item.AverageRating != null && item.AverageRating >= 0) ? item.AverageRating : "N/A"} </TableCell>
            </TableRow>
          ))
    );
  }
}