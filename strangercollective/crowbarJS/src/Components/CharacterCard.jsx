import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class AttributeCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{color:"#FFF"}}> <table style={{width:'100%'}}><tr><td style={{width:'100%',paddingLeft:8}}>{this.props.json.firstname} {this.props.json.lastname}</td><td>{this.props.json.cost}</td></tr></table> </span>
        </div>
        <div style={{padding:8}}>
       
      </div>
      </Paper>
    );
  }
}

export default AttributeCard;
