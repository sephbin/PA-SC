import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class MainCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8, height:"100%"}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> </span>
        </div>
        <div style={{padding:8}}>
         {JSON.stringify(this.props.json)}
      </div>
      </Paper>
    );
  }
}

export default MainCard;
