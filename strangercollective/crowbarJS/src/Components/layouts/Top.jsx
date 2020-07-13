import React, { Component } from 'react';
import Button from '../Button'


class Top extends Component {
  render() {
const style = {
	position: 'fixed',
	top: 0,
	left: 0,
	right: 0,
	height: this.props.json.layout.universal.sideWidth,
	backgroundColor: '#222'
};
    return (
      <div style={style}>
      </div>
    );
  }
}

export default Top;
