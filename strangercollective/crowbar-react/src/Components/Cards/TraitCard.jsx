import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import CardHeader from './CardHeader';
import CardContent from './CardContent';

class TraitCard extends Component {
  constructor(props) {
    super(props);
  }

  render() {
  const selector = this.props.cardArray
  const mapOb = this.props.character[selector]; 
    return (
      <div className="card">
        <CardHeader cardTitle={this.props.cardTitle} modal="advantages"/>
        <CardContent>
      <table className="trait-table">
      {mapOb.map( (ad, i) => {
        return (
        <tr>
        <td style={{width: '100%'}}>{ad.name}</td>
        <td style={{textAlign: "right"}}>[{ad.cost}]</td>
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

TraitCard.propTypes = {
  character: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
});

export default connect(mapStateToProps, {})(TraitCard);