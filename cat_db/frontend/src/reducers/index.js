import { combineReducers } from "redux";
import breedReducer from "./reducers";

export default combineReducers({
  entries: breedReducer
});
