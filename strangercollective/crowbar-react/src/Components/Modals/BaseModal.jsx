import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { __addpossession__, __changeinput__} from '../../Actions/Actions';

class BaseModal extends Component {
  constructor(props) {
	super(props);
    this.addItem = this.addItem.bind(this);
    this.onChange = this.onChange.bind(this);
	}
	addItem(e) {
	    console.log("Clicked");
	    console.log(this.props.character.id);
	    this.props.__addpossession__("2");
	}
	onChange(e) {
    var a = e.target.value;
    var i = e.target.getAttribute("index");
    this.props.__changeinput__(i,a);
	}

  render() {
  	const style = {
    };
    return (
      <div className="modal-background possessions">
        <div className="modal-wrapper">
        <div className="modal-header">Edit Possessions</div>
        <div className="modal-content">
        <table className="trait-table">
        <tr>
        <td></td>
        <td></td>	
        <td className="right" ><b>Wt</b></td>
        <td className="right" ><b>$</b></td>
        <td className="right" ></td>
        </tr>
      {this.props.character.relpossession.map( (sk, i) => {
        console.log(i); 
        return (
        <tr key={i}>
        <td className="nowrap" ><input type='number' value={sk.ammount} className="ammount"/>x </td>
        <td className="wide" ><input index={i} onChange={this.onChange} list="possessionslist" value={sk.possession.possession_name} /></td>
        <td className="right" >{sk.weight}</td>
        <td className="right" >{sk.cost}</td>
        <td className="right" ><span className="badge">x</span></td>
        </tr>
          )
        }
      )
      }
      <tr>
        <th colspan={4} ></th>
        <th className="right" ><span onClick={this.addItem} className="badge">+</span></th>
      </tr>
      <tr>
        <th colspan={2} className="right">Total</th>
        <th>{this.props.character.possessionTotals.weight}</th>
        <th>{this.props.character.possessionTotals.cost}</th>
        <th></th>
      </tr>
      </table>
        </div>
        </div>
<datalist id="possessionslist">
	<option value="Internet Explorer" />
	<option value="Firefox" />
	<option value="Chrome" />
	<option value="Opera" />
	<option value="Safari" />
</datalist>
      </div>
    );
  }
}

BaseModal.propTypes = {
	__addpossession__: PropTypes.func.isRequired,
	__changeinput__: PropTypes.func.isRequired,
	character: PropTypes.object.isRequired,
	con: PropTypes.array.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
  con: state.reducedata.consoleText,
});

export default connect(mapStateToProps, {__addpossession__, __changeinput__})(BaseModal);