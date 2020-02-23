import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Instructions = () => {
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: 50, width: "100%"}}>
      <Link to="/">
        <FontAwesome name="back" className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
    <div>
      <h1 style={{ textAlign: "center"}}>Instructions</h1>
      <br />
      <ul>
        <li>Learn about quantum game theory by playing classical game theory games using quantum methods!</li>
        <li>First, choose if you would like to play on a simulator or real quantum computer, then select the protocol, game theory game and how many people will play.</li>
        <li>Each player will get a chance to drag their selected gates onto the circuit whilst the other players cannot see your selection. Use the quantum gates to optimise your strategy against the other players and aim to maximise your payoff to win the game!</li>
      </ul>
      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/settings">
          <Button color="link" style={{color: "#212529"}}>
            Next
          </Button>
        </Link>
      </div>
    </div>
    </div>
  );
}

export default Instructions;
