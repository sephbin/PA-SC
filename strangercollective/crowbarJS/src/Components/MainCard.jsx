import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

// <div dangerouslySetInnerHTML={{__html: this.props.json.characterPage.mainContents}} />
class MainCard extends Component {
  render() {
    const style = {
    };
    return (
      <Paper style={{marginBottom:8, height:"100%"}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> </span>
        </div>
        <div style={{padding:8, wordWrap: 'break-word', height: 'calc(100% - 3em)', overflowY: 'auto'}}>
         <pre dangerouslySetInnerHTML={{__html: JSON.stringify(this.props.json, null, 2)}} />
      </div>
      </Paper>
    );
  }
}

export default MainCard;