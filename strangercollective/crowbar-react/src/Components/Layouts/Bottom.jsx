import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { __changeCharacter__} from '../../Actions/Actions';

class Bottom extends Component {
	constructor(props) {
		super(props);
    this.onChange = this.onChange.bind(this);
	}
	onChange(e) {
    var a = e.target.value;
    console.log("What is a");
    if (a == "") {a = 0};
    if (a < 0) {a = 0};
    if (a > this.props.charactersLength) {a = this.props.charactersLength};
    console.log(a);
    this.props.__changeCharacter__(a);
	}

  render() {

    return (
      <div className="bottom layout">
      <table className="console">
      <tr>
      <td width="100%">>> {this.props.consoleText.slice(-1).pop()}</td>
      <td><input style={{width:"3em", textAlign:"center"}} min={0} max={this.props.charactersLength} type="number" onChange={this.onChange} value={this.props.selectCharacter}/></td>
      </tr>
      </table>
      </div>
    );
  }
}

Bottom.propTypes = {
__changeCharacter__: PropTypes.func.isRequired,
  consoleText: PropTypes.array.isRequired
}

const mapStateToProps = state => ({
  consoleText: state.reducedata.consoleText,
  selectCharacter: state.reducedata.selectCharacter,
  charactersLength: (state.reducedata.characters.length)-1,
});

export default connect(mapStateToProps, {__changeCharacter__})(Bottom);
