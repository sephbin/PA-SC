import React, { Component } from 'react';

class Button extends Component {
  render() {
	const style = {
		width: this.props.appState.layout.universal.sideWidth,
		height: this.props.appState.layout.universal.sideWidth,
		backgroundImage: "url('"+this.props.json.image+"')",
		backgroundSize: "70%",
		backgroundRepeat: "no-repeat",
		backgroundPosition: "center",
		cursor: "pointer",
	};
    return (
      <div style={style} title={this.props.json.tooltip}>
      </div>
    );
  }
}

export default Button;
