import React, { Component } from "react";
import Modal from "react-modal";
import "./App.css";

import AddBreed from "./components/AddBreed";
import Entries from "./components/Entries";

class App extends Component {
  constructor() {
    super();
    this.state = {
      entries: [],
      showModal: false
    };

    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
  }

  handleOpenModal() {
    this.setState({ showModal: true });
    console.log("open modal");
  }

  handleCloseModal() {
    this.setState({ showModal: false });
  }

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
          <Entries entries={this.state.entries} />
        </div>
        <br></br>
        <div className="container">
          <button className="btn btn-primary" onClick={this.handleOpenModal}>
            Add a Breed
          </button>
          <Modal
            isOpen={this.state.showModal}
            onRequestClose={this.handleCloseModal}
          >
            <div className="container">
              <h1>Add A Breed</h1>
              <AddBreed />
              <br></br>
              <button
                className="btn btn-primary"
                onClick={this.handleCloseModal}
              >
                Close
              </button>
            </div>
          </Modal>
        </div>
      </div>
    );
  }
}

export default App;
