import React, {Component} from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Entries from "./Entries";

class App extends Component {

  state = {
    entries: []
    };

  componentDidMount() {
    fetch('http://localhost:8000/breeds/')
    .then(res => res.json())
    .then((data) => {
      this.setState({ entries: data })
      })
    .catch(console.log)
    }

  render() {
    return (
      <Contacts contacts={this.state.contacts}/>
      );
    }
}

export default App;