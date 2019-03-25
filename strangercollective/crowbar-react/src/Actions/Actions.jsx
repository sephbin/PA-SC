import {
__ACTION1__,
__ACTION2__,
__ACTION3__,
__CHANGECHARACTER__,
__ADDPOSSESSION__,
__CHANGEINPUT__,
__TOGGLEMODAL__
} from './Types';

export const __action1__ = () => dispatch => {
    // fetch('http://www.strangercollective.com/rpg/characters/')
		fetch('http://localhost:8000/rpg/campaigns/1/')
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
      });
};


export const __changeCharacter__ = (newSelector) => dispatch => {
dispatch({
        type: __CHANGECHARACTER__,
        payload: newSelector
      });
};

export const __addpossession__ = (characterid) => dispatch => {
    fetch('http://localhost:8000/rpg/api/newpos/'+characterid, {
      method: 'GET',
    })
      .then(result => result.json())
      .then(data => dispatch({
        type: __ADDPOSSESSION__,
        payload: data
      }));
};

export const __changeinput__ = (input,value) => dispatch => {
dispatch({
        type: __CHANGEINPUT__,
        payload: {input: input, value: value}
      });
};

export const __togglemodal__ = (modal) => dispatch => {
dispatch({
        type: __TOGGLEMODAL__,
        payload: {'modal': modal}
      });
};