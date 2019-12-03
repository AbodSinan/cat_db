import React, { Component } from "react";

class AddBreed extends Component {
  render() {
    return (
      <form
        action="/breeds/"
        method="POST"
        encType="multipart/form-data"
        className="form-horizontal"
        noValidate=""
      >
        <fieldset>
          <input
            type="hidden"
            name="csrfmiddlewaretoken"
            value="y01bmGws5eEY82SX09SQILga3NO5JSozUmXM2mWiGxcEzmO8eyKIq5GUpINMexxV"
          />
          <div className="form-group ">
            <label className="col-sm-2 control-label ">ID</label>
            <div className="col-sm-10">
              <input
                name="ID"
                className="form-control"
                type="number"
                value=""
              />
            </div>
          </div>
          <div className="form-group">
            <label className="col-sm-2 control-label ">User</label>
            <div className="col-sm-10">
              <select className="form-control" name="user">
                <option value="1">admin</option>
              </select>
            </div>
          </div>

          <div className="form-group ">
            <label className="col-sm-2 control-label ">Name</label>
            <div className="col-sm-10">
              <input
                name="name"
                className="form-control"
                type="text"
                value=""
                placeholder="Name"
              ></input>
            </div>
          </div>

          <div className="form-group ">
            <label className="col-sm-2 control-label ">Origin</label>
            <div className="col-sm-10">
              <input
                name="origin"
                className="form-control"
                type="text"
                value=""
                placeholder="Origin"
              ></input>
            </div>
          </div>

          <div className="form-group ">
            <label className="col-sm-2 control-label ">Description</label>
            <div className="col-sm-10">
              <textarea
                placeholder="Describe your Breed"
                name="description"
                className="form-control"
              ></textarea>
            </div>
          </div>

          <div className="form-actions">
            <button
              className="btn btn-primary"
              title=""
              data-original-title="Make a POST request on the Breed List resource"
              onClick={() => {
                console.log("posting");
              }}
            >
              POST
            </button>
          </div>
        </fieldset>
      </form>
    );
  }
}

export default AddBreed;
