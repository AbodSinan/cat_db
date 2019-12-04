export const ADD_BREED = "ADD_BREED";
export const ADD_HOME = "ADD_HOME";
export const ADD_HUMAN = "ADD_HUMAN";
export const ADD_CAT = "ADD_CAT";

export function addBreed(ID, origin, description, name, user) {
  return {
    type: ADD_BREED,
    ID: ID,
    origin: origin,
    description: description,
    name: name,
    user: user
  };
}

export function addHome(ID, name, address, home_type, user) {
  return {
    type: ADD_HOME,
    ID: ID,
    name: name,
    address: address,
    home_type: home_type,
    user: user
  };
}

export function addHuman(
  ID,
  name,
  date_of_birth,
  gender,
  description,
  home,
  user
) {
  return {
    type: ADD_HUMAN,
    ID: ID,
    name: name,
    date_of_birth: date_of_birth,
    gender: gender,
    description: description,
    home: home,
    user: user
  };
}

export function addCats(
  ID,
  name,
  breed,
  owner,
  date_of_birth,
  description,
  user
) {
  return {
    TYPE: ADD_CATS,
    ID: ID,
    name: name,
    breed: breed,
    owner: owner,
    date_of_birth: date_of_birth,
    description: description,
    user: user
  };
}
