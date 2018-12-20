import React, { Component, Fragment } from 'react';
import Top from './layouts/Top' 
import Bottom from './layouts/Bottom' 
import Left from './layouts/Left' 
import Right from './layouts/Right' 
import Content from './layouts/Content' 


class App extends Component {
	constructor(props) {
		super(props);

		this.state = {
			"page":"CharacterPage",
			"characterList": [],
			"characterPage":{
				"mainContents":"<h1>HELLO</h1>This is rendering some extra HTML"
			},
			"character":{
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
			"bm":5,
			"reladvantage":[],
			"reldisadvantage":[],
			"relskill":[],
			"languages":[],
			"relpossession":[],
			"possessionTotals":{"cost":0,"weight":0},
			// "melee":[{"meleestats":[]}],
			// "ranged":[{"rangestats":[]}],
		},
			"layout":{"universal":{"sideWidth":"2.3em"},"left":[
				{"tooltip":"Characters","image":"https://image.flaticon.com/icons/svg/149/149910.svg"},
				// {"tooltip":"Characters","image":"https://image.flaticon.com/icons/svg/1152/1152840.svg"},
				// {"tooltip":"Button 2","image":"https://image.flaticon.com/icons/svg/1152/1152810.svg"},
				// {"tooltip":"Button 3","image":"https://image.flaticon.com/icons/svg/1152/1152833.svg"},
				// {"tooltip":"Button 4","image":"https://image.flaticon.com/icons/svg/1152/1152812.svg"}
			]
		}};
	
	}
	

componentDidMount() {
  this.timer = setInterval(()=> this.getItems(), 60000);
}

componentWillUnmount() {
  this.timer = null; // here...
}

getItems() {
    fetch('http://www.strangercollective.com/rpg/characters/2')
      .then(response => response.json())
      .then(character => this.setState({ character }))
      .then(character => console.log(character))
      .catch(error => console.log("error",error));
	}
	


	eventFunction = (charid) => {
	fetch('http:/www.strangercollective.com/rpg/characters/'+charid)
      .then(response => response.json())
      .then(character => this.setState({ character }))
      .then(character => console.log(character))
      .then(this.setState({page: "CharacterPage" }))
      .catch(error => console.log("error",error));		
    console.log(charid);
	}
  render() {
    return (
      <Fragment>
      {/*<button onClick={() => this.eventFunction()}>Hello</button>*/}
      <Top json={this.state}/>
      <Left json={this.state}/>
      <Right json={this.state}/>
      <Bottom json={this.state}/>
      <Content json={this.state} func={this.eventFunction}/>
      </Fragment>
    );
  }
}

export default App;
