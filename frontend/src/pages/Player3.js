import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Player3 = () => {
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: "5%", width: "100%"}}>
      <Link to="/player2">
        <FontAwesome className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
      <div style={{position: "fixed", top: 40, left: "95%", width: "100%"}}>
      <Link to="/settings">
        <FontAwesome className="fas fa-cog fa-lg" style={{color: "#212529"}}/>
      </Link>        
      </div>
    <div>
      <h1 style={{ textAlign: "center"}}>Player 3</h1>
      <br />
      Test
      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/player4">
          <Button color="link" style={{color: "#212529"}}>
            Next
          </Button>
        </Link>
      </div>
    </div>
    </div>
  );
}

export default Player3;