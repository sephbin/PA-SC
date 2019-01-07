import React, { Component } from 'react';
import { Provider } from 'react-redux';
import ExampleComponent from './Components/ExampleComponent';
import Store from './Store.jsx';




class ExampleApp extends Component {

  render() {
    return (
    	<Provider store={Store}>
      <div className="App">
      <ExampleComponent />
      </div>
      </Provider>
    );
  }
}

export default ExampleApp;
