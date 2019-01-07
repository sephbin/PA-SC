import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import CardHeader from './CardHeader';
import CardContent from './CardContent';


class SkillCard extends Component {
  render() {

    return (
      <div className="card">
        <CardHeader cardTitle="Skills"/>
      <CardContent>
      <table className="trait-table">
      {this.props.character.relskill.map( (sk, i) => {
        
        return (
        <tr>
        <td style={{whiteSpace:"nowrap"}}><b>{sk.relative_value}</b> - </td>
        <td style={{width: '100%'}}>{sk.skill.skill_name}</td>
        <td>{sk.challenge}</td>
        <td>{sk.relative}</td>
        <td style={{textAlign: "right"}}>[{sk.cost}]</td>
        </tr>
          )
        }
      )
      }
      </table>
      </CardContent>
      </div>
    );
  }
}

SkillCard.propTypes = {
  character: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
});

export default connect(mapStateToProps, {})(SkillCard);