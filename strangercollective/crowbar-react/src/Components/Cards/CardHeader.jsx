import React, { Component } from 'react';

class CardHeader extends Component {
  constructor(props) {
  super(props);
  }
  render() {
    console.log(this.props);
    return (
      <div className="card-header">
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

export default CardHeader;
