import {
  ADD_BREED,
  ADD_HOME,
  ADD_CAT,
  ADD_HUMAN,
  TRIGGER_MODAL,
  FETCH_BREEDS
} from "../actions/types";

const initialState = {
  modalIsOn: false,
  breeds: [],
  cats: [],
  humans: [],
  homes: []
};

export default function(state = initialState, action) {
  console.log("reached reducer with type of" + action.type);
  switch (action.type) {
    case ADD_BREED:
      return {
        ...state,
        breeds: [...state.breeds, action.payload]
      };

    case ADD_HOME:
      return {
        ...state,
        homes: [...state.homes, action.payload]
      };
    case ADD_HUMAN:
      return {
        ...state,
        humans: [...state.humans, action.payload]
      };
    case ADD_CAT:
      return {
        ...state,
        cats: [...state.cats, action.payload]
      };
    case FETCH_BREEDS:
      console.log("reached update reducer");
      return {
        ...state,
        breeds: action.payload
      };

    case TRIGGER_MODAL:
      return {
        ...state,
        modalIsOn: action.payload
      };
    default:
      console.log("returning default state");
      return state;
  }
}
