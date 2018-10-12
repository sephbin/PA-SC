import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class LaguageCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Laguages </span>
        </div>
        <div style={{padding:8}}>
        <table style={{width:"100%"}}>
        <tr>
          <th></th>
          <th style={{width:"20%"}}>Written</th>
          <th style={{width:"20%"}}>Spoken</th>
          <th></th>
          </tr>
      {this.props.json.map( (ad, i) => {
        let bwidth = 1
        if (i === (this.props.json.length - 1)) {
          bwidth = 0
        }
        return (
        <tr>
        <td style={{width: '50%', borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{ad.language}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{ad.written}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{ad.spoken}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>[{ad.cost}]</td>
        </tr>
          )
        }
      )
      }
      </table>
      </div>
      </Paper>
    );
  }
}

export default LaguageCard;
