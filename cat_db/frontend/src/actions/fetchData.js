import {
  ADD_BREED,
  ADD_CAT,
  ADD_HOME,
  ADD_HUMAN,
  FETCH_BREEDS,
  TRIGGER_MODAL
} from "./types";

export const fetchBreeds = () => dispatch => {
  console.log("Fetching data");
  fetch("http://localhost:8000/breeds/")
    .then(res => res.json())
    .then(breeds =>
      dispatch({
        type: FETCH_BREEDS,
        payload: breeds
      })
    );
};

export function addBreed(data) {
  return {
    type: ADD_BREED,
    payload: data
  };
}

export function addHome(data) {
  return {
    type: ADD_HOME,
    payload: data
  };
}

export function addHuman(data) {
  return {
    type: ADD_HUMAN,
    payload: data
  };
}

export function addCats(data) {
  return {
    type: ADD_CAT,
    payload: data
  };
}

export const triggerModal = isOn => {
  return {
    type: TRIGGER_MODAL,
    payload: isOn
  };
};
