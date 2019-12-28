import React, { useState } from 'react';

import { Link } from 'react-router-dom'
import { Button, ButtonGroup } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Settings = () => {
  const [ProtocolSelected, setProtocolSelected] = useState(null);
  const [GameSelected, setGameSelected] = useState(null);
  const [PlayersSelected, setPlayersSelected] = useState(null);
  const [PayoffSelected, setPayoffSelected] = useState(null);


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
        <ButtonGroup>
          <Button color="primary" onClick={() => setProtocolSelected('EWL')} active={ProtocolSelected === 'EWL'}>EWL</Button>
          <Button color="primary" onClick={() => setProtocolSelected('MW')} active={ProtocolSelected === 'MW'}>MW</Button>
        </ButtonGroup>
        <p>Selected: {ProtocolSelected}</p>

        <h4>Game</h4>
        <ButtonGroup>
          <Button color="primary" onClick={() => setGameSelected('Prisoners')} active={GameSelected === 'Prisoners'}>Prisoners</Button>
          <Button color="primary" onClick={() => setGameSelected('Minority')} active={GameSelected === 'Minority'}>Minority</Button>
          <Button color="primary" onClick={() => setGameSelected('BoS')} active={GameSelected === 'Bos'}>Bos</Button>
        </ButtonGroup>
        <p>Selected: {GameSelected}</p>

        <h4>Players</h4>
        <ButtonGroup>
          <Button color="primary" onClick={() => setPlayersSelected(1)} active={PlayersSelected === 1}>1</Button>
          <Button color="primary" onClick={() => setPlayersSelected(2)} active={PlayersSelected === 2}>2</Button>
          <Button color="primary" onClick={() => setPlayersSelected(3)} active={PlayersSelected === 3}>3</Button>
          <Button color="primary" onClick={() => setPlayersSelected(4)} active={PlayersSelected === 4}>4</Button>
        </ButtonGroup>
        <p>Selected: {PlayersSelected}</p>

        <h4>Payoff</h4>
        <ButtonGroup>
          <Button color="primary" onClick={() => setPayoffSelected('Defined')} active={PayoffSelected === 'Defined'}>Defined</Button>
          <Button color="primary" onClick={() => setPayoffSelected('Custom')} active={PayoffSelected === 'Custom'}>Custom</Button>
        </ButtonGroup>
        <p>Selected: {PayoffSelected}</p>

      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/player1">
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