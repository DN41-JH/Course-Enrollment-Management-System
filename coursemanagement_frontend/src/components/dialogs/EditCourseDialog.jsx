// Obtained as "Form Dialogs" from Material-UI: https://material-ui.com/components/dialogs/

import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { CourseService } from '../../services/CourseService';
// import { JwtService } from '../../services/JwtService';
// import cookie from 'react-cookies';


export default function EditCourseDialog(props) {
  const [editField, setEditField] = useState(null);
  const [newContent, setNewContent] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  function edit() {
    const editCourseInfo = {
        courseId: props.course.CourseId,
        instrucotrId: parseInt(window.sessionStorage.getItem("Id")),
        targetField: editField,
        newContent: newContent,
    };
    
    CourseService.editCourse(editCourseInfo)
      .then(response => {
        window.location.reload();
      })
      .catch(error => {
        props.onErrorMessageChange(error.response.data.response.error);
      })
      .finally(() => setIsLoading(false));
  }

  return (
    <div>
      <Dialog open={props.open} onClose={props.onClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title"> Edit Course </DialogTitle>
        <DialogContent>
          <TextField
            required
            margin="dense"
            id="username"
            label="Target Field (i.e. 'Course', 'Title')"
            type="username"
            fullWidth
            onChange={(event) => setEditField(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="password"
            label="New Content"
            type="username"
            fullWidth
            onChange={(event) => setNewContent(event.target.value)}
            disable={isLoading}
          />
          <DialogContentText color="error">
            {props.errorMessage}
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={edit} color="primary" disable={isLoading}> Submit </Button>
          <Button onClick={props.onClose} color="primary" disable={isLoading}> Cancel </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}