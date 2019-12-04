import { ADD_BREED, ADD_HOME, ADD_CAT, ADD_HUMAN } from "../actions/actions";

const initialState = {
    states = [
        breeds = [],
        cats = [],
        humans = [],
        homes = []
    ]

};

function rootReducer(state = initialState, action){
    switch(action.type) {
        case ADD_BREED:
            return {
                ...states,
                breeds :
                [
                    ...state.breeds,
                    {
                        ID: action.ID,
                        origin: action.origin,
                        description: action.description,
                        name: action.name,
                        user: action.user
                    }
                ] 
            };
            
        case ADD_HOME:
            return{
                ...states,
                homes : 
                [
                    ...state.homes,
                    {
                    ID: action.ID,
                    name: action.name,
                    address: action.address,
                    home_type: action.home_type,
                    user: action.user
                    }
                ]
            };
            case ADD_HUMAN:
                    return{
                        ...states,
                        humans : 
                        [
                            ...state.humans,
                            {
                                ID: action.ID,
                                name: action.name,
                                date_of_birth: action.date_of_birth,
                                gender: action.gender,
                                description: action.description,
                                home: action.home,
                                user: action.user
                            }
                        ]
                    };
            case ADD_CAT:
                return{
                    ...states,
                    cats:
                    [
                        ...state.cats,
                        {
                            ID: action.ID,
                            name: action.name,
                            breed: action.breed,
                            owner: action.owner,
                            date_of_birth: action.date_of_birth,
                            description: action.description,
                            user: action.user  
                        }
                    ]
                };
            default:
                return state
    };

    

}

export default rootReducer;