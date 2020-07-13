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
        let row
        if (sk.possession.rangeStatsText != '') {
        row = (<tr>
          <td colspan={99}>{sk.possession.possession_name}</td>
          </tr>);
        }
        return (
        <Fragment>
        {row}
        {/*<tr>{JSON.stringify(sk)}</tr>*/}
        {sk.rangeStats.map(( st, j ) => {return (
          <Fragment>
            <tr style={{borderBottomWidth: 1, borderBottomStyle:"solid", borderBottomColor:"rgba(0,0,0,0.2)"}}>
              <td style={{whiteSpace: 'nowrap'}}><b>{st.value} -</b></td>
              <td colspan={1}>{st.damageStats.stType}:</td>
              <td style={{width:'100%'}} colspan={99}>{st.damage}</td>
            </tr>
            <tr className="details">
              <td></td>
              <td colspan={99}>
                <table style={{width:"100%"}}>
                  <tr>
                    <td>Acc</td>
                    <td>Range</td>
                    <td>RoF</td>
                    <td>Shots</td>
                    <td>Strength</td>
                    <td>Rcl</td>
                    <td>Bulk</td>
                    <td>Notes</td>
                  </tr>
                  <tr>
                    <td>{st.accuracy}</td>
                    <td>{st.range}</td>
                    <td>{st.rateOfFire}</td>
                    <td>{st.shots}</td>
                    <td>{st.strength}</td>
                    <td>{st.rcl}</td>
                    <td>{st.bulk}</td>
                    <td>{st.notes}</td>
                  </tr>
                </table>
              </td>
            </tr>
          </Fragment> )} )}
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
