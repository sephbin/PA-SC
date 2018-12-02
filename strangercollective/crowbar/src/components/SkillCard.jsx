import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class SkillCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Skills </span>
        </div>
        <div style={{padding:8}}>
      <table style={{width:"100%"}}>
      {this.props.json.map( (sk, i) => {
        let bwidth = 1
        if (i === (this.props.json.length - 1)) {
          bwidth = 0
        }
        return (
        <tr>
        <td style={{borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)", whiteSpace:"nowrap"}}><b>{sk.relative_value}</b> - </td>
        <td style={{width: '100%', borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.skill.skill_name}</td>
        <td style={{borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.challenge}</td>
        <td style={{borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.relative}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>[{sk.cost}]</td>
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

export default SkillCard;
