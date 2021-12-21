// Obtained from Material-UI: https://material-ui.com/components/alert/#alert

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Alert from '@material-ui/lab/Alert';
import IconButton from '@material-ui/core/IconButton';
import Collapse from '@material-ui/core/Collapse';
import CloseIcon from '@material-ui/icons/Close';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    '& > * + *': {
      marginTop: theme.spacing(2),
    },
  },
}));

export default function ActionAlert(props) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Collapse in={props.open}>
        <Alert
          severity={props.alertSeverity}
          action={
            <IconButton
              aria-label="close"
              color="inherit"
              size="small"
              onClick={() => props.onAlertClick()}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
        >
          {props.alertMessage}
        </Alert>
      </Collapse>
    </div>
  );
}
