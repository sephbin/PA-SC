import { __ACTION1__, __ACTION2__, __ACTION3__ } from '../Actions/Types';


const initialState = {
	items: [],
	item: 0
}

export default function(state = initialState, action) {
	switch (action.type) {
		case __ACTION1__:
		console.log('reducer dispatched');
			return {
				...state,
				items: action.payload,
				item: 999
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
		default:
			return state;
	}
}