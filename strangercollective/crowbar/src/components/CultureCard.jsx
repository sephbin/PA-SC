import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class CultureCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Cultures </span>
        </div>
        <div style={{padding:8}}>
      </div>
      </Paper>
    );
  }
}

export default CultureCard;