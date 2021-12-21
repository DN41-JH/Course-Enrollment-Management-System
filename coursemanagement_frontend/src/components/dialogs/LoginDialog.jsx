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
import { UserService } from '../../services/UserService';
// import cookie from 'react-cookies';


export default function LoginDialog(props) {

  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  return (
    <div>
      <Dialog open={props.open} onClose={props.onClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title"> Login </DialogTitle>
        <DialogContent>
          <TextField
            required
            margin="dense"
            id="username"
            label="Username"
            type="username"
            fullWidth
            onChange={(event) => setUsername(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="password"
            label="Password"
            type="password"
            fullWidth
            onChange={(event) => setPassword(event.target.value)}
            disable={isLoading}
          />
          <DialogContentText color="error">
            {props.errorMessage}
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={login} color="primary" disable={isLoading}> Login </Button>
          <Button onClick={props.onClose} color="primary" disable={isLoading}> Cancel </Button>
        </DialogActions>
      </Dialog>
    </div>
  );

  function login() {
        // send request to server (username + password)
        // 1. if succeed, store the JWT token in cookie
        // 2. if failed, show an error message
        setIsLoading(true);

        // JwtService.login(username, password)  // Obtains a promise (either success with a "response" or fail with an "error")
        // .then(response => {
        //     cookie.save(JWT_TOKEN_COOKIE_NAME, response.data.access);
        //     window.location.reload();
        // })
        // .catch(error => {
        //     console.log(error.response.data.detail);
        //     setErrorMessage(error.response.data.detail);
        // })
        // .finally(() => setIsLoading(false));

        const loginInfo = {
            username: username,
            password: password,
        };
        
        UserService.login(loginInfo)
        .then(response => {
          window.sessionStorage.setItem("Id", response.data.response.ID);
          window.sessionStorage.setItem("Role", response.data.response.Role);
          window.location.reload();
        })
        .catch(error => {
          props.onErrorMessageChange(error.response.data.response.error);
        })
        .finally(() => setIsLoading(false));
  }
}