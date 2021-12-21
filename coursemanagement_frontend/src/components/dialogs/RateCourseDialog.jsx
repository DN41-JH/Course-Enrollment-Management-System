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


export default function RateCourseDialog(props) {
  const [rating, setRating] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  return (
    <div>
      <Dialog open={props.open} onClose={props.onClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title"> Rate the Course </DialogTitle>
        <DialogContent>
          <TextField
            required
            margin="dense"
            id="rating"
            label="Give Your Rating as an Integer Between 0 and 10"
            type="username"
            fullWidth
            onChange={(event) => setRating(event.target.value)}
            disable={isLoading}
          />
          <DialogContentText color="error">
            {props.errorMessage}
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={rateCourse} color="primary" disable={isLoading}> Submit </Button>
          <Button onClick={props.onClose} color="primary" disable={isLoading}> Cancel </Button>
        </DialogActions>
      </Dialog>
    </div>
  );

  function rateCourse() {
        setIsLoading(true);

        const rateCourseInfo = {
            studentId: parseInt(window.sessionStorage.getItem("Id")),
            courseId: props.course.CourseId,
            rating: rating,
        };
        
       CourseService.rateCourse(rateCourseInfo)
        .then(response => {
          window.location.reload();
        })
        .catch(error => {
          props.onErrorMessageChange(error.response.data.response.error);
        })
        .finally(() => setIsLoading(false));
  }
}