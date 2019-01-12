import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { __addpossession__, __changeinput__, __togglemodal__} from '../../Actions/Actions';

class PossessionModal extends Component {
  constructor(props) {
	super(props);
    this.addItem = this.addItem.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onExit = this.onExit.bind(this);
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
  onExit(e){
    this.props.__togglemodal__("possessions");
  }

  render() {
  	const style = {
    };
    return (
      <div className={"modal-background possessions "+this.props.display} >
        <div className="modal-wrapper">
        <div className="modal-header"><table width="100%"><tr><td width="100%">Edit Possessions</td><td onClick={this.onExit}>X</td></tr></table></div>
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
{this.props.possessions.map( (sk, i) => {
	return (
  <option value={sk.possession_name} />
  )
  })}
</datalist>
      </div>
    );
  }
}

PossessionModal.propTypes = {
	__addpossession__: PropTypes.func.isRequired,
  __changeinput__: PropTypes.func.isRequired,
	__togglemodal__: PropTypes.func.isRequired,
  character: PropTypes.object.isRequired,
  possessions: PropTypes.array.isRequired,
	display: PropTypes.string.isRequired,
	con: PropTypes.array.isRequired,
}

const mapStateToProps = state => ({
  character: state.reducedata.displayCharacter,
  possessions: state.reducedata.possessions,
  display: state.reducedata.page.modals.possessions,
  con: state.reducedata.consoleText,
});

export default connect(mapStateToProps, {__addpossession__, __changeinput__,__togglemodal__})(PossessionModal);