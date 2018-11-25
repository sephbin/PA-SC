import React, { Component, Fragment } from 'react';
import Paper from '@material-ui/core/Paper';

class MeleeCard extends Component {
  render() {
  	const style = {
    };
    return (
      <Paper style={{marginBottom:8}}>
        <div style={{backgroundColor:"#F00"}}>
          <span style={{paddingLeft:8, color:"#FFF"}}> Melee </span>
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
        {sk.meleestats.map(( st, j ) => {return (<Fragment><tr style={{borderBottomWidth: 1, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>
          <td style={{whiteSpace: 'nowrap'}}><span>v</span> <b>{st.value} -</b></td>
          <td style={{width:'100%'}} colspan={99}>{sk.name}: {st.damage}</td>
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

export default MeleeCard;
