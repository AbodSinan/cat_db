import React, { Component } from "react";
import Modal from "react-modal";
import { connect } from "react-redux";

import AddBreed from "./AddBreed";
import Entries from "./Entries";
import { triggerModal } from "../actions/fetchData";
import PropTypes from "prop-types";

class Breeds extends Component {
  handleCloseModal() {
    this.props.triggerModal(false);
  }
  handleOpenModal() {
    this.props.triggerModal(true);
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
        <br></br>
        <div className="container">
          <button className="btn btn-primary" onClick={this.handleOpenModal}>
            Add a Breed
          </button>
          <Modal
            isOpen={this.props.isModalOn}
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

Entries.propTypes = {
  triggerModal: PropTypes.func.isRequired
};

const mapStatesToProps = state => ({
  isModalOn: state.entries.isModalOn
});

export default connect(mapStatesToProps, { triggerModal })(Breeds);
