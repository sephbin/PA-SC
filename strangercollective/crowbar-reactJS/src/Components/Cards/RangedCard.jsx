import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import CardHeader from './CardHeader';
import CardContent from './CardContent';


class RangedCard extends Component {
  render() {
  	const style = {
    };
    return (
      <div className="card">
        <CardHeader cardTitle="Ranged"/>
        <div style={{padding:8}}>
        <table style={{width:"100%"}}>
      {this.props.character.relpossession.map( (sk, i) => {
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
      </div>
    );
  }
}

RangedCard.propTypes = {
  character: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
});

export default connect(mapStateToProps, {})(RangedCard);