import {
	__ACTION1__,
	__ACTION2__,
	__ACTION3__,
	__CHANGECHARACTER__,
	__ADDPOSSESSION__,
	__CHANGEINPUT__,
	__TOGGLEMODAL__,
} from '../Actions/Types';


const initialState = {
	displayCharacter: {
		reladvantage: [],
		reldisadvantage: [],
		relskill: [],
		relpossession: [],
		possessionTotals:{},
	},
	selectCharacter: 1,
	items: [],
	characters: [{}],
	possessions: [{}],
	item: 0,
	consoleText: [],
	page:{
		modals: {
			advantages: 'hidden',
			possessions: 'hidden'
		}
	}
}

export default function(state = initialState, action) {
	switch (action.type) {
		case __ACTION1__:
		console.log('reducer dispatched');
			return {
				...state,
				characters: action.payload.character,
				displayCharacter: action.payload.character[initialState.selectCharacter],
				possessions: action.payload.possession,
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
		case __CHANGEINPUT__:
			let chars = state.characters;
			var dChar = chars[state.selectCharacter];
			dChar.relpossession[action.payload.input].possession.possession_name = action.payload.value
			return {
				...state,
				characters: chars,
				displayCharacter: chars[state.selectCharacter],
				consoleText: initialState.consoleText.concat(["Changing Value"]),
			};
		case __ADDPOSSESSION__:
			let __ap__chars = state.characters;
			__ap__chars[state.selectCharacter] = action.payload;
			return {
				...state,
				characters: __ap__chars,
				displayCharacter: action.payload,
				consoleText: initialState.consoleText.concat(["Added Possession"]),
			};
		case __TOGGLEMODAL__:
			let __tm__page = state.page;
			if (__tm__page.modals[action.payload.modal] == 'hidden') {
			__tm__page.modals[action.payload.modal] = 'visible';
			}else{
			__tm__page.modals[action.payload.modal] = 'hidden';
		}
			return {
				...state,
				page: __tm__page

			};
		default:
			return state;
	}
}