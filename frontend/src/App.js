import React from 'react';

import HomePage from './pages/Home.js'
import InstructionPage from './pages/Instructions.js'
import SettingPage from './pages/Settings.js'
import Player1Page from './pages/Player1.js'
import Player2Page from './pages/Player2.js'
import Player3Page from './pages/Player3.js'
import Player4Page from './pages/Player4.js'
import ResultsPage from './pages/Results.js'


import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import { Container, Row, Col } from 'reactstrap';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import './App.css';


const App = () => {
  return (
    <Container>
        <Row>
          <Col sm="12" md={{ size: 8, offset: 2 }}>
            <Router>
              <Switch>
                <Route exact path="/">
                  <HomePage />
                </Route>
                <Route path="/instructions">
                  <InstructionPage />
                </Route>
                <Route path="/settings">
                  <SettingPage />
                </Route>
                <Route path="/player1">
                  <Player1Page />
                </Route>
                <Route path="/player2">
                  <Player2Page />
                </Route>
                <Route path="/player3">
                  <Player3Page />
                </Route>
                <Route path="/player4">
                  <Player4Page />
                </Route>
                <Route path="/results">
                  <ResultsPage />
                </Route>
              </Switch>
            </Router>
          </Col>
        </Row>
    </Container>
  );
}

export default App;
