import React, { Component, Fragment } from 'react';
import Paper from '@material-ui/core/Paper';

class RangedCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Ranged </span>
        </div>
        <div style={{padding:8}}>
        <table style={{width:"100%"}}>
      {this.props.json.map( (sk, i) => {
        let bwidth = 1
        if (i === (this.props.json.length - 1)) {
          bwidth = 0
        }
        return (
        <Fragment>
        {/*<tr>{JSON.stringify(sk.rangestats)}</tr>*/}
        {sk.rangestats.map(( st, j ) => {return (<Fragment><tr style={{borderBottomWidth: 1, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>
          <td style={{whiteSpace: 'nowrap'}}><span>v</span> <b>{st.value} -</b></td>
          <td style={{width:'100%'}} colspan={99}>{sk.name}: {st.damage}</td>
          </tr>
          <tr style={{textAlign:"right"}}>
            <td></td>
            <td>Range</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>RoF</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>Bulk</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>Rcl</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>St</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>Shots</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>Acc</td>
            <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>Notes</td>
          </tr>
          <tr style={{textAlign:"right"}}>
          {/*style={{display:"none"}}*/}
          <td></td>
          <td>{st.range}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.rateOfFire}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.bulk}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.rcl}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.strength}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.shots}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.accuracy}</td>
          <td style={{borderLeftWidth: 1, borderLeftStyle:"solid", borderLeftColor:"rgba(0,0,0,0.2)"}}>{st.notes}</td>
          </tr></Fragment> )} )}
        </Fragment>

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

export default RangedCard;
