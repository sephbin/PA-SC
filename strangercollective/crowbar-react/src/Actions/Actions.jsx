import { __ACTION1__, __ACTION2__, __ACTION3__, __CHANGECHARACTER__ } from './Types';

export const __action1__ = () => dispatch => {
		fetch('http://www.strangercollective.com/rpg/characters/')
  		.then(result => result.json())
  		.then(data => dispatch({
  			type: __ACTION1__,
  			payload: data
  		}));
};

export const __action2__ = (postData) => dispatch => {
fetch('https://jsonplaceholder.typicode.com/users', {
      method: 'POST',
      headers: {
        'content-type': 'application/json'
      },
      body: JSON.stringify(postData)
    })
      .then(result => result.json())
      .then(data => dispatch({
      	type: __ACTION2__,
      	payload: data
      }));
};

export const __action3__ = (address, postData) => dispatch => {
console.log(postData);
dispatch({
        type: __ACTION3__,
        payload: {}
      })
};


export const __changeCharacter__ = (newSelector) => dispatch => {
dispatch({
        type: __CHANGECHARACTER__,
        payload: newSelector
      })
};

