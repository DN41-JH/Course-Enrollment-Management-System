// Obtained as "Form Dialogs" from Material-UI: https://material-ui.com/components/dialogs/

import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import StudentTable from '../tables/StudentTable';
// import { JwtService } from '../../services/JwtService';
// import cookie from 'react-cookies';


export default function ViewCourseStudentsDialog(props) {
  return (
    <div>
      <Dialog open={props.open} onClose={props.onClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title"> Enrolled Students </DialogTitle>

        <DialogContent>
          <StudentTable
            students={props.courseStudents}
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={props.onClose} color="primary"> Close </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}