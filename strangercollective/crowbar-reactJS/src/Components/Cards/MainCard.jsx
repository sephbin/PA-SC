import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

// <div dangerouslySetInnerHTML={{__html: this.props.json.characterPage.mainContents}} />
class MainCard extends Component {
  render() {
    return (
      <Fragment>
      <pre dangerouslySetInnerHTML={{__html: JSON.stringify(this.props.item, null, 2)}} />
      </Fragment>
    );
  }
}

MainCard.propTypes = {
  item: PropTypes.object
}

const mapStateToProps = state => ({
  item: state
});

export default connect(mapStateToProps, {})(MainCard);
