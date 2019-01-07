import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import CardHeader from './CardHeader';
import CardContent from './CardContent';

class PossesionCard extends Component {
  render() {
  	const style = {
    };
    return (
      <div className="card">
        <CardHeader cardTitle="Possessions"/>
        <div style={{padding:8}}>
        <table className="trait-table">
        <tr>
        <td></td>
        <td></td>
        <td style={{textAlign: "right"}}>Wt</td>
        <td style={{textAlign: "right"}}>$</td>
        </tr>
      {this.props.character.relpossession.map( (sk, i) => {
              
        return (
        <tr>
        <td style={{whiteSpace:"nowrap"}}><b>{sk.ammount}</b>x </td>
        <td style={{width: '100%'}}>{sk.possession.possession_name}</td>
        <td style={{textAlign: "right"}}>{sk.weight}</td>
        <td style={{textAlign: "right"}}>{sk.cost}</td>
        </tr>
          )
        }
      )
      }
      <tr>
        <th colspan={2} style={{textAlign: "left"}}>Total</th>
        <th>{this.props.character.possessionTotals.weight}</th>
        <th>{this.props.character.possessionTotals.cost}</th>
      </tr>
      </table>
      </div>
      </div>
    );
  }
}

PossesionCard.propTypes = {
  character: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
});

export default connect(mapStateToProps, {})(PossesionCard);