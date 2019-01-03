import { __ACTION1__, __ACTION2__, __ACTION3__, __CHANGECHARACTER__ } from '../Actions/Types';


const initialState = {
	displayCharacter: {},
	selectCharacter: 0,
	items: [],
	characters: [{}],
	item: 0,
	consoleText: []
}

export default function(state = initialState, action) {
	switch (action.type) {
		case __ACTION1__:
		console.log('reducer dispatched');
			return {
				...state,
				characters: action.payload,
				displayCharacter: action.payload[initialState.selectCharacter],
				item: 999,
				consoleText: initialState.consoleText.concat(["Welcome to Crowbar"])
			};
		case __ACTION2__:
			return {
				...state,
				item: action.payload
			};
		case __ACTION3__:
			console.log(action.payload);
			return {
				...state,
				items : [{"id":2,"conditions":[{"id":4,"condition_text_html":"Example Text","condition_satisfied":true,"condition_proof":null,"condition_heirachy":1,"parent":2}]}],
				item: 555
			};
		case __CHANGECHARACTER__:
			return {
				...state,
				selectCharacter :parseInt(action.payload),
				displayCharacter: state.characters[parseInt(action.payload)],
				consoleText: initialState.consoleText.concat(["Changed character to " + state.characters[parseInt(action.payload)].firstname]),
			};
		default:
			return state;
	}
}