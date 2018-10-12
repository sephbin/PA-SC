import React, { Component } from 'react';
import Button from '../Button'


class Right extends Component {
  render() {
const style = {
	position: 'fixed',
	top: this.props.json.layout.universal.sideWidth,
	bottom: 0,
	right: 0,
	width: this.props.json.layout.universal.sideWidth,
	backgroundColor: '#222'
};
    return (
      <div style={style}>
      </div>
    );
  }
}

export default Right;
