import React, { Component } from 'react';


class TraitCard extends Component {
  render() {
  	const style = {
    };

    return (
      <div className="Card">
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> {this.props.cardTitle} </span>
        </div>
        <div style={{padding:8}}>
      <table style={{width:"100%"}}>
      {this.props.json.map( (ad, i) => {
        let bwidth = 1
        if (i === (this.props.json.length - 1)) {
          bwidth = 0
        }
        return (
        <tr>
        <td style={{width: '100%', borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>{ad.name}</td>
        <td style={{textAlign: "right", borderBottomWidth: bwidth, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>[{ad.cost}]</td>
        </tr>
          )
        }
      )
      }
      </table>
      </div>
      </div>
    );
  }
}

export default TraitCard;
