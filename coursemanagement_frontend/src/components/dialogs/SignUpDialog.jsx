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

export default function SignUpDialog(props) {
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);
  const [firstname, setFirstname] = useState(null);
  const [lastname, setLastname] = useState(null);
  const [email, setEmail] = useState(null);
  const [department, setDepartment] = useState(null);
  const [role, setRole] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  function checkMissingField() {
    return (username && password && firstname && lastname && email && department && role) ? false : true;
  }

  function register() {
        if (checkMissingField()) {
            props.onErrorMessageChange("Missing registration information(s).");
            return;
        }

        setIsLoading(true);

        const registerInfo = {
            username: username,
            password: password,
            firstname: firstname,
            lastname: lastname,
            email: email,
            department: department,
            role: role,
        };
        
        UserService.register(registerInfo)
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
        <DialogTitle id="form-dialog-title"> Sign Up </DialogTitle>
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
          <TextField
            required
            margin="dense"
            id="firstname"
            label="First Name"
            type="username"
            fullWidth
            onChange={(event) => setFirstname(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="lastname"
            label="Last Name"
            type="username"
            fullWidth
            onChange={(event) => setLastname(event.target.value)}
            disable={isLoading}
          />
          <TextField
            margin="dense"
            id="email"
            label="Email"
            type="email"
            fullWidth
            onChange={(event) => setEmail(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="department"
            label="Department Name"
            type="username"
            fullWidth
            onChange={(event) => setDepartment(event.target.value)}
            disable={isLoading}
          />
          <TextField
            required
            margin="dense"
            id="role"
            label="Role (either Student or Instructor)"
            type="username"
            fullWidth
            onChange={(event) => setRole(event.target.value)}
            disable={isLoading}
          />

          <DialogContentText color="error">
            {props.errorMessage}
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={register} color="primary" disable={isLoading}> Register </Button>
          <Button onClick={props.onClose} color="primary" disable={isLoading}> Cancel </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}