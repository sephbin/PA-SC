import React, { Component } from 'react';
import Button from '../Button'


class Top extends Component {
  render() {
const style = {
	position: 'fixed',
	top: this.props.json.layout.universal.sideWidth,
	left: 0,
	bottom: 0,
	width: this.props.json.layout.universal.sideWidth,
	backgroundColor: '#222'
};
    return (
      <div style={style}>
      {this.props.json.layout.left.map(b =>
      <Button json={b} appState={this.props.json} />
        )}
      </div>
    );
  }
}

export default Top;
