import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import CardHeader from './CardHeader';
import CardContent from './CardContent';

class CharacterCard extends Component {
  constructor(props) {
    super(props);
    }
    

  render() {
    return (
      <div className="card">
      <CardHeader cardTitle={(this.props.character.firstname +" "+ this.props.character.lastname)} cardCost={this.props.character.cost}>Inner Html</CardHeader>
      <CardContent>
      {this.props.character.occupation}
      </CardContent>
      </div>
    );
  }
}

CharacterCard.propTypes = {
  character: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
});

export default connect(mapStateToProps, {})(CharacterCard);
