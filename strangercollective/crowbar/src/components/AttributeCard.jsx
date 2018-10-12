import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class AttributeCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Attributes </span>
        </div>
        <div style={{padding:8}}>
      <table style={{width:"100%"}}>
      <tr style={{height:"2em", textAlign:"center"}}>
      <td><b>ST</b></td> <td>{this.props.json.attributes.st}</td><td>[0]</td>
      <td><b>HP</b></td> <td>{this.props.json.attributes.hp}</td><td>[0]</td>
      <td><b>SM</b></td> <td>{this.props.json.attributes.sm}</td><td>[0]</td>
      </tr>
      <tr style={{height:"2em", textAlign:"center"}}>
      <td><b>DX</b></td><td>{this.props.json.attributes.dx}</td><td>[0]</td>
      <td><b>Per</b></td><td>{this.props.json.attributes.per}</td><td>[0]</td>
      <td><b>BS</b></td><td>{this.props.json.attributes.bs}</td><td>[0]</td>
      </tr>
      <tr style={{height:"2em", textAlign:"center"}}>
      <td><b>IQ</b></td><td>{this.props.json.attributes.iq}</td><td>[0]</td>
      <td><b>Will</b></td><td>{this.props.json.attributes.will}</td><td>[0]</td>
      <td><b>BM</b></td><td>{this.props.json.attributes.bm}</td><td>[0]</td>
      </tr>
      <tr style={{height:"2em", textAlign:"center"}}>
      <td><b>HT</b></td><td>{this.props.json.attributes.ht}</td><td>[0]</td>
      <td><b>FP</b></td><td>{this.props.json.attributes.fp}</td><td>[0]</td>
      </tr>
      </table>
      </div>
      </Paper>
    );
  }
}

export default AttributeCard;
