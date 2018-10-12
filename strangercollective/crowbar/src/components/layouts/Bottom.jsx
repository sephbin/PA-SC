import React, { Component } from 'react';
import Button from '../Button'



class Bottom extends Component {
  render() {
const style = {
	position: 'fixed',
	bottom: 0,
	left: this.props.json.layout.universal.sideWidth,
	right: this.props.json.layout.universal.sideWidth,
	height: this.props.json.layout.universal.sideWidth,
 	width: '100%',
  color: "#FFF",
	backgroundColor: '#222'
};
    return (
      <div style={style}>
      Console:
      </div>
    );
  }
}

export default Bottom;
