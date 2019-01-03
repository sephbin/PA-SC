import React, { Component } from 'react';


class PossesionCard extends Component {
  render() {
  	const style = {
    };
    return (
      <div className="Card">
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
        <td style={{width: '100%', borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.possession.possession_name}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.weight}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{sk.cost}</td>
        </tr>
          )
        }
      )
      }
      <tr>
        <th colspan={2} style={{textAlign: "left"}}>Total</th>
        <th>{this.props.char.possessionTotals.weight}</th>
        <th>{this.props.char.possessionTotals.cost}</th>
      </tr>
      </table>
      </div>
      </div>
    );
  }
}

export default PossesionCard;
