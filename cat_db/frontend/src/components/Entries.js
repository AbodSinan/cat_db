import React from "react";


const Entries = ({ entries }) => {

  const handleClick = userID => {
    const requestOptions = {
      method : 'DELETE',
    };

    fetch("http://localhost:8000/breeds/" + userID, requestOptions).then((response) => {
      return response.json();
    }).then((result) => {
      console.log("deleted")
    })
  };

  return (
    <div className ="list-group">
      <center><h1>Breed List</h1></center>
      {entries.map((entry) => (
        <div className="list-group-item list-group-item-action flex-column align-items-start" style = {{backgroundColor : 'green'}} key={entry.ID} onClick={() => handleClick(entry.ID)}>
          <div className="list-group-item">
            <h5 className="mb-1">{entry.name}</h5>
            <h6 className="mb-1">{entry.origin}</h6>
            <small>{entry.description}</small>
          </div>
        </div>
      ))}
    </div>
  )
};

export default Entries;