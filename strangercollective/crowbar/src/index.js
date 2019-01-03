import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import registerServiceWorker from './registerServiceWorker';
// import App from './Components/App';
import ExampleApp from './ExampleApp';

// ReactDOM.render(<App />, document.getElementById('root'));
ReactDOM.render(<ExampleApp />, document.getElementById('root'));
registerServiceWorker();
