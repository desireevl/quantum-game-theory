import React, { useState } from 'react';

import HomePage from './pages/Home.js'
import InstructionPage from './pages/Instructions.js'
import SettingPage from './pages/Settings.js'
import PlayerPage from './pages/Player.js'
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
  const [protocolSelected, setProtocolSelected] = useState('EWL');
  const [gameSelected, setGameSelected] = useState('minority');
  const [playersSelected, setPlayersSelected] = useState(4);
  const [deviceSelected, setDeviceSelected] = useState('simulator');
  const [payoffSelected, setPayoffSelected] = useState('Defined');

  const [playerData, setPlayerData] = useState({})

  const appState = {
    settings: {
      protocolSelected,
      gameSelected,
      playersSelected,
      deviceSelected,
      payoffSelected
    },
    playerData
  }

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
                  <SettingPage
                    appState={appState}
                    setProtocolSelected={setProtocolSelected}
                    setGameSelected={setGameSelected}
                    setPlayersSelected={setPlayersSelected}
                    setDeviceselected={setDeviceSelected}
                    setPayoffSelected={setPayoffSelected}
                  />
                </Route>
                <Route path="/player">
                  <PlayerPage
                    appState={appState}
                    setPlayerData={setPlayerData}
                  />
                </Route>
                <Route path="/results">
                  <ResultsPage
                    appState={appState}
                   />
                </Route>
              </Switch>
            </Router>
          </Col>
        </Row>
    </Container>
  );
}

export default App;
