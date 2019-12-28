import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Player3 = () => {
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
    <div>
      <h1 style={{ textAlign: "center"}}>Results</h1>
      <br />
      Test
      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/">
          <Button color="link" style={{color: "#212529"}}>
            Play Again
          </Button>
        </Link>
      </div>
    </div>
    </div>
  );
}

export default Player3;