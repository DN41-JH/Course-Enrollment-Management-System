// Obtained as "Form Dialogs" from Material-UI: https://material-ui.com/components/dialogs/

import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
// import { JwtService } from '../../services/JwtService';
import { UserService } from '../../services/UserService';
// import cookie from 'react-cookies';


export default function WithdrawDialog(props) {
  const [isLoading, setIsLoading] = useState(false);

  function withdraw() {
    setIsLoading(true);

    const withdrawInfo = {
        Id: window.sessionStorage.getItem("Id"),
        Role: window.sessionStorage.getItem("Role"),
    };
    
    UserService.withdraw(withdrawInfo)
    .then(response => {
        window.sessionStorage.removeItem("Id");
        window.sessionStorage.removeItem("Role");
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
        <DialogTitle id="form-dialog-title"> Withdraw </DialogTitle>

        <DialogContent>
            <DialogContentText color="error">
                Do you want to withdraw yourself from the system?
                Please do notice that this is irreversible.
            </DialogContentText>
        </DialogContent>

        <DialogContentText color="error">
          {props.errorMessage}
        </DialogContentText>

        <DialogActions>
          <Button onClick={withdraw} color="primary" disable={isLoading}> Confirm </Button>
          <Button onClick={props.onClose} color="primary" disable={isLoading}> Cancel </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}