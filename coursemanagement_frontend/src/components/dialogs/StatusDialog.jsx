// Obtained as "Form Dialogs" from Material-UI: https://material-ui.com/components/dialogs/

import React, { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
// import { JwtService } from '../../services/JwtService';
import { UserService } from '../../services/UserService';
// import cookie from 'react-cookies';


export default function StatusDialog(props) {
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    getStatus();
  });

  function getStatus() {
    const checkStatusInfo = {
        Id: parseInt(window.sessionStorage.getItem("Id")),
        Role: window.sessionStorage.getItem("Role"),
    };
    
    UserService.checkStatus(checkStatusInfo)
    .then(response => {
        setStatusMessage(`Your Name: ${response.data.FirstName + ' ' + response.data.LastName}. You are logged in as: ${window.sessionStorage.getItem("Role")}. Your Department: ${response.data.DepartmentName}. Total Credit Hours: ${response.data.TotalCredit}.`);
    })
    .catch(error => {
      setStatusMessage(error.response.data.response.error);
    })
  }

  return (
    <div>
      <Dialog open={props.open} onClose={props.onClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title"> Your Status </DialogTitle>
        <DialogContent>
          <DialogContentText>
            {statusMessage}
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={props.onClose} color="primary"> OK </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}