import React, { Component } from 'react';
import Button from '../Button'


class Left extends Component {
  render() {
    return (
      <div className="left layout">
      {[].map(b =>
      <Button json={b} appState={this.props.json} />
        )}
      </div>
    );
  }
}

export default Left;
