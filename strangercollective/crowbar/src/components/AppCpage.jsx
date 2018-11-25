import React, { Component, Fragment } from 'react';
import Top from './layouts/Top' 
import Bottom from './layouts/Bottom' 
import Left from './layouts/Left' 
import Right from './layouts/Right' 
import Content from './layouts/Content' 


class App extends Component {
	constructor(props) {
		super(props);

		this.state = {"character":{"attributes":{
			"st":10,
			"dx":10,
			"iq":10,
			"ht":10,
			"hp":10,
			"per":10,
			"will":10,
			"fp":10,
			"sm":1,
			"bs":5,
			"bm":5
		},
			"advantages":[],
			"disadvantages":[],
			"skills":[],
			"languages":[],
		},
			"layout":{"universal":{"sideWidth":"2.3em"},"left":[
				// {"tooltip":"Button 1","image":"https://image.flaticon.com/icons/svg/1152/1152840.svg"},
				// {"tooltip":"Button 2","image":"https://image.flaticon.com/icons/svg/1152/1152810.svg"},
				// {"tooltip":"Button 3","image":"https://image.flaticon.com/icons/svg/1152/1152833.svg"},
				// {"tooltip":"Button 4","image":"https://image.flaticon.com/icons/svg/1152/1152812.svg"}
			]
		}};
	}
	componentDidMount() {
	console.log("ATTEMPT FETCH")
    fetch('http://localhost:8000/rpg/character/2')
      .then(response => response.json())
      .then(character => this.setState({ character }))
      .then(character => console.log(character))
      .catch(error => console.log("error",error));
      // .then(response => console.log("Complete"))
	}
	



  render() {
    return (
      <Fragment>
      <Top json={this.state}/>
      <Left json={this.state}/>
      <Right json={this.state}/>
      <Bottom json={this.state}/>
      <Content json={this.state}/>
      </Fragment>
    );
  }
}

export default App;
