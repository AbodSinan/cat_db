import React from "react";


const Entries = ({ entries }) => {
  return (
    <div>
      <center><h1>Contact List</h1></center>
      {entries.map((entry) => (
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{contact.name}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{contact.origin}</h6>
            <p class="card-text">{contact.description}</p>
          </div>
        </div>
      ))}
    </div>
  )
};

export default Entries;