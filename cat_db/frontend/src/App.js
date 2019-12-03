import React, { Component } from "react";
import "./App.css";

import AddBreed from "./components/AddBreed";
import Entries from "./components/Entries";

class App extends Component {
  state = {
    entries: []
  };
  componentDidMount() {
    console.log("fetching......");
    fetch("http://localhost:8000/breeds/")
      .then(res => res.json())
      .then(data => {
        this.setState({ entries: data });
      })
      .catch(console.log);
  }

  render() {
    return (
      <div className="main-container">
        <div className="container">
          <Entries entries={this.state.entries} onPress />
        </div>
        <br></br>
        <div className="container">
          <AddBreed />
        </div>
      </div>
    );
  }
}

export default App;
