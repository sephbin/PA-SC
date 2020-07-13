import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { __togglemodal__} from '../../Actions/Actions';

class CardHeader extends Component {
  constructor(props) {
  super(props);
    this.togModal = this.togModal.bind(this);
  }
  togModal(e){
    this.props.__togglemodal__(this.props.modal);
  }

  render() {
    console.log(this.props);
    return (
      <div className="card-header" onClick={this.togModal}>
          <span>
            <table className="card-header-table">
              <tr>
                <td className="card-header-title">{this.props.cardTitle}</td>
                <td className="card-header-cost">{this.props.cardCost}</td>
              </tr>
            </table>
          </span>
      </div>
    );
  }
}

CardHeader.propTypes = {
  __togglemodal__: PropTypes.func.isRequired
}

const mapStateToProps = state => ({
});

export default connect(mapStateToProps, {__togglemodal__})(CardHeader);