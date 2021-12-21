// Obtained as "Form Dialogs" from Material-UI: https://material-ui.com/components/dialogs/

import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
// import { JwtService } from '../../services/JwtService';
import { CourseService } from '../../services/CourseService';
// import cookie from 'react-cookies';

export default function NewCourseDialog(props) {
  const [number, setNumber] = useState(null);
  const [title, setTitle] = useState(null);
  const [section, setSection] = useState(null);
  const [type, setType] = useState(null);
  const [creditHour, setCreditHour] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [daysOfWeek, setDaysOfWeek] = useState(null);
  const [room, setRoom] = useState(null);
  const [building, setBuilding] = useState(null);
  const [capacity, setCapacity] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  function checkMissingField() {
    return (number && title && section && type && creditHour && startTime && endTime && daysOfWeek && room && building && capacity) ? false : true;
  }

  function create() {
        if (checkMissingField()) {
            props.onErrorMessageChange("Missing new course information(s).")
            return;
        }

        setIsLoading(true);

        const newCourseInfo = {
            number: number,
            title: title,
            section: section,
            type: type,
            creditHour: parseInt(creditHour),
            startTime: startTime,
            endTime: endTime,
            daysOfWeek: daysOfWeek,
            room: room,
            building: building,
            capacity: parseInt(capacity),
            instructorId: parseInt(window.sessionStorage.getItem("Id")),
        };
        
        CourseService.createCourse(newCourseInfo)
          .then(response => {
              window.location.reload();
          })
          .catch((error) => {
              props.onErrorMessageChange(error.response.data.response.error);
          })
          .finally(() => setIsLoading(false));
  }

  return (
    <div>
      <Dialog open={props.open} onClose={props.onClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title"> Add New Course </DialogTitle>
        <DialogContent>
          <TextField
            required
            margin="dense"
            id="number"
            label="Course Number (i.e. 'CS 411')"
            type="username"
            fullWidth
            onChange={(event) => setNumber(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="title"
            label="Course Title"
            type="username"
            fullWidth
            onChange={(event) => setTitle(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="section"
            label="Course Section"
            type="username"
            fullWidth
            onChange={(event) => setSection(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="type"
            label="Course Type (i.e. 'LEC', 'DIS', 'LAB')"
            type="username"
            fullWidth
            onChange={(event) => setType(event.target.value)}
            disable={isLoading}
          />
          <TextField
            margin="dense"
            id="creditHour"
            label="Course Credit Hour"
            type="number"
            fullWidth
            onChange={(event) => setCreditHour(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="startTime"
            label="Start Time (i.e. '11:00 AM')"
            type="username"
            fullWidth
            onChange={(event) => setStartTime(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="endTime"
            label="End Time (i.e. '12:20 PM')"
            type="username"
            fullWidth
            onChange={(event) => setEndTime(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="daysOfWeek"
            label="Days Of Week (i.e. 'MWF')"
            type="username"
            fullWidth
            onChange={(event) => setDaysOfWeek(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="room"
            label="Room Number (i.e. 1002)"
            type="username"
            fullWidth
            onChange={(event) => setRoom(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="building"
            label="Building (i.e. 'ECEB')"
            type="username"
            fullWidth
            onChange={(event) => setBuilding(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="capacity"
            label="Course Capacity"
            type="username"
            fullWidth
            onChange={(event) => setCapacity(event.target.value)}
            disable={isLoading}
          />

          <DialogContentText color="error">
            {props.errorMessage}
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={create} color="primary" disable={isLoading}> Add Course </Button>
          <Button onClick={props.onClose} color="primary" disable={isLoading}> Cancel </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}