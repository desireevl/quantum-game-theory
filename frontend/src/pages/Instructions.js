import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Instructions = () => {
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: 50, width: "100%"}}>
      <Link to="/">
        <FontAwesome className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
    <div>
      <h1 style={{ textAlign: "center"}}>Instructions</h1>
      <br />
      <ul>
        <li>Learn about quantum game theory by playing games!</li>
        <li>Choose a game, protocol or custom payoff table</li>
        <li>Choose a number of players</li>
        <li>Play the game by dragging your selected gates onto the circuit</li>
        <li>View your results!</li>
      </ul>
      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/instructions">
          <Button color="link" style={{color: "#212529"}}>
            Play
          </Button>
        </Link>
      </div>
    </div>
    </div>
  );
}

export default Instructions;