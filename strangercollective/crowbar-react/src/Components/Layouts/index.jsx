import React, { Component, Fragment } from 'react';
// 
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { __action1__} from '../../Actions/Actions';
// 
import './Layout.css';
import Top from './Top' 
import Bottom from './Bottom' 
import Left from './Left' 
import Right from './Right' 
import Content from './Content' 


class Layout extends Component {
constructor(props) {
    super(props);
  }

  componentWillMount(){
    this.props.__action1__();
  }
  render() {
    return (
      <Fragment>
      <Top />
      <Left />
      <Right />
      <Bottom />
      <Content />
      </Fragment>
    );
  }
}

Layout.propTypes = {
  __action1__: PropTypes.func.isRequired,
}

const mapStateToProps = state => ({
});

export default connect(mapStateToProps, {__action1__})(Layout);