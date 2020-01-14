import React, { useState } from 'react';

import { Link } from 'react-router-dom'
import { Button, ButtonToolbar } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Settings = (props) => {
  const { 
    appState, 
    setProtocolSelected,
    setGameSelected,
    setPlayersSelected,
    setPayoffSelected
  } = props
  const { settings } = appState

  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: 50, width: "100%"}}>
      <Link to="/instructions">
        <FontAwesome className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
    <div>
      <h1 style={{ textAlign: "center"}}>Settings</h1>
      <br />
        <h4>Protocol</h4>
        <ButtonToolbar>
          <Button color="primary" onClick={() => setProtocolSelected('EWL')} active={settings.protocolSelected === 'EWL'}>EWL</Button>
          <Button color="primary" onClick={() => setProtocolSelected('MW')} active={settings.protocolSelected === 'MW'}>MW</Button>
        </ButtonToolbar>
        <br />

        <h4>Game</h4>
        <ButtonToolbar>
          <Button color="primary" onClick={() => setGameSelected('Prisoners')} active={settings.gameSelected === 'Prisoners'}>Prisoners</Button>
          <Button color="primary" onClick={() => setGameSelected('Minority')} active={settings.gameSelected === '4-minority'}>Minority</Button>
          <Button color="primary" onClick={() => setGameSelected('BoS')} active={settings.gameSelected === 'Bos'}>Bos</Button>
        </ButtonToolbar>
        <br />

        <h4>Players</h4>
        <ButtonToolbar>
          <Button color="primary" onClick={() => setPlayersSelected(1)} active={settings.playersSelected === 1}>1</Button>
          <Button color="primary" onClick={() => setPlayersSelected(2)} active={settings.playersSelected === 2}>2</Button>
          <Button color="primary" onClick={() => setPlayersSelected(3)} active={settings.playersSelected === 3}>3</Button>
          <Button color="primary" onClick={() => setPlayersSelected(4)} active={settings.playersSelected === 4}>4</Button>
        </ButtonToolbar>
        <br />

        <h4>Payoff</h4>
        <ButtonToolbar>
          <Button color="primary" onClick={() => setPayoffSelected('Defined')} active={settings.payoffSelected === 'Defined'}>Defined</Button>
          <Button color="primary" onClick={() => setPayoffSelected('Custom')} active={settings.payoffSelected === 'Custom'}>Custom</Button>
        </ButtonToolbar>

      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/player">
          <Button color="link" style={{color: "#212529"}}>
            Play
          </Button>
        </Link>
      </div>
    </div>
    </div>
  );
}

export default Settings;