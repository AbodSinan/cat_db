import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { Provider } from "react-redux";

import Breeds from "./components/Breeds";
import Homes from "./components/Homes";
import Cats from "./components/Cats";
import Humans from "./components/Humans";
import store from "./store/store";

export default function App() {
  return (
    <Provider store={store}>
      <Router>
        <div>
          <nav className="navbar navbar-light navbar-expand-lg bg-light">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link to="/breeds">
                  <span className="nav-link">Breeds</span>
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/cats">
                  <span className="nav-link">Cats</span>
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/homes">
                  <span className="nav-link">Homes</span>
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/humans">
                  <span className="nav-link">Humans</span>
                </Link>
              </li>
            </ul>
          </nav>
          <Switch>
            <Route path="/breeds">
              <Breeds path="/breeds/" title="Breed" />
            </Route>
            <Route path="/humans">
              <Humans path="/humans/" title="Human" />
            </Route>
            <Route path="/homes">
              <Homes path="/homes/" title="Home" />
            </Route>
            <Route path="/cats">
              <Cats path="/cats/" title="Cat" />
            </Route>
          </Switch>
        </div>
      </Router>
    </Provider>
  );
}
