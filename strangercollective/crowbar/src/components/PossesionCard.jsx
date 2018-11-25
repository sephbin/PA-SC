import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';

class PossesionCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Possesions </span>
        </div>
        <div style={{padding:8}}>
        <table style={{width:"100%"}}>
        <tr>
        <td></td>
        <td></td>
        <td style={{textAlign: "right"}}>Wt</td>
        <td style={{textAlign: "right"}}>$</td>
        </tr>
      {this.props.json.map( (sk, i) => {
        let bwidth = 1
        
        return (
        <tr>
        <td style={{borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)", whiteSpace:"nowrap"}}><b>{sk.ammount}</b>x </td>
        <td style={{width: '100%', borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.name}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.weight}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.cost}</td>
        </tr>
          )
        }
      )
      }
      <tr>
        <th colspan={2} style={{textAlign: "left"}}>Total</th>
        <th>{this.props.char.possessionsTotals.weight}</th>
        <th>{this.props.char.possessionsTotals.cost}</th>
      </tr>
      </table>
      </div>
      </Paper>
    );
  }
}

export default PossesionCard;
