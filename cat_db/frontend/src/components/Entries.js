import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchBreeds } from "../actions/fetchData";
import PropTypes from "prop-types";

class Entries extends Component {
  componentDidMount() {
    this.props.fetchBreeds();
  }

  handleClick(userID) {
    const requestOptions = {
      method: "DELETE"
    };

    fetch("http://localhost:8000" + this.props.path + userID, requestOptions)
      .then(response => {
        return response.json();
      })
      .then(result => {
        console.log("deleted");
      });
  }

  render() {
    console.log(this.props);
    return (
      <div className="list-group">
        {this.props.breeds.map(entry => (
          <div
            className="list-group-item list-group-item-action flex-column align-items-start"
            style={{ backgroundColor: "green" }}
            key={entry.ID}
            onClick={this.handleClick(entry.ID)}
          >
            <div className="list-group-item">
              <ul>
                {Object.values(entry).map(function(item) {
                  if (!Array.isArray(item)) {
                    return (
                      <li key={item} className="mb-1">
                        {item}
                      </li>
                    );
                  }
                })}
              </ul>
            </div>
          </div>
        ))}
      </div>
    );
  }
}

Entries.propTypes = {
  fetchBreeds: PropTypes.func.isRequired,
  breeds: PropTypes.array.isRequired
};

const mapStateToProps = state => ({
  breeds: state.entries.breeds,
  isModalOpen: state.entries.modalIsOn
});

export default connect(mapStateToProps, { fetchBreeds })(Entries);
