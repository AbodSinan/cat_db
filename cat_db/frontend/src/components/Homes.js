import React, { Component } from "react";

import Entries from "./Entries";

class Homes extends Component {
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
    fetch("http://localhost:8000" + this.props.path)
      .then(res => res.json())
      .then(data => {
        this.setState({ entries: data });
      })
      .catch(console.log);
  }

  render() {
    return (
      <div className="main-container">
        <center>
          <h1>{this.props.title} List</h1>
        </center>
        <div className="container">
          <Entries path={this.props.path} />
        </div>
      </div>
    );
  }
}

export default Homes;
