import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import CardHeader from './CardHeader';
import CardContent from './CardContent';

class AttributeCard extends Component {
  render() {
    return (
      <div className="card">
        <CardHeader cardTitle="Attributes"/>
      <CardContent>
        <table style={{width:"100%"}}>
        <tr style={{height:"2em", textAlign:"center"}}>
        <td><b>ST</b></td> <td>{this.props.character.st}</td><td>[0]</td>
        <td><b>HP</b></td> <td>{this.props.character.hp}</td><td>[0]</td>
        <td><b>SM</b></td> <td>{this.props.character.sm}</td><td>[0]</td>
        </tr>
        <tr style={{height:"2em", textAlign:"center"}}>
        <td><b>DX</b></td><td>{this.props.character.dx}</td><td>[0]</td>
        <td><b>Per</b></td><td>{this.props.character.per}</td><td>[0]</td>
        <td><b>BS</b></td><td>{this.props.character.bs}</td><td>[0]</td>
        </tr>
        <tr style={{height:"2em", textAlign:"center"}}>
        <td><b>IQ</b></td><td>{this.props.character.iq}</td><td>[0]</td>
        <td><b>Will</b></td><td>{this.props.character.will}</td><td>[0]</td>
        <td><b>BM</b></td><td>{this.props.character.bm}</td><td>[0]</td>
        </tr>
        <tr style={{height:"2em", textAlign:"center"}}>
        <td><b>HT</b></td><td>{this.props.character.ht}</td><td>[0]</td>
        <td><b>FP</b></td><td>{this.props.character.fp}</td><td>[0]</td>
        </tr>
        </table>
      </CardContent>
      </div>
    );
  }
}

AttributeCard.propTypes = {
  character: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
});

export default connect(mapStateToProps, {})(AttributeCard);
