import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { __action1__, __action3__ } from '../Actions/Actions';

class Basic extends Component {
constructor(props) {
    super(props);
  }

  componentWillMount(){
    this.props.__action1__();
  }
  // componentDidMount() {
  //   this.timer = setInterval(() => this.props.__action1__(), 1000)
  // }

  render() {
    // const postItems = JSON.stringify(this.props)
  	const postItems = "";
    
    return (
  	<Fragment>
  		<div> { JSON.stringify(this.props)}</div>
		</Fragment>
    );
  }
}

Basic.propTypes = {
  __action1__: PropTypes.func.isRequired,
  __action3__: PropTypes.func.isRequired,
  itemarray: PropTypes.array.isRequired,
  item: PropTypes.object
}

const mapStateToProps = state => ({
  itemarray: state.reducedata.items,
  item: state.reducedata.item
});

export default connect(mapStateToProps, {__action1__, __action3__})(Basic);
