import React, { Component } from 'react';
import { Provider } from 'react-redux';
import Basic from './Components/Basic';
import Layouts from './Components/Layouts';
import Store from './Store.jsx';




class App extends Component {

  render() {
    return (
		<Provider store={Store}>
		<Layouts />
		</Provider>
    );
  }
}

export default App;
