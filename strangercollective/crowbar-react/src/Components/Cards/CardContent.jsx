import React, { Component } from 'react';

class CardContent extends Component {
  constructor(props) {
  super(props);
  }
  render() {
    return (
      <div className="card-content">
        {this.props.children}
      </div>
    );
  }
}

export default CardContent;
