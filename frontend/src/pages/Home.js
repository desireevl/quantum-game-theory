import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';

const Home = () => {
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div>
        <h1 style={{ textAlign: "center"}}>Quantum Game Theory</h1>
        <br />
        <h4 style={{ textAlign: "justify"}}>Learn about quantum computing and game theory by playing classical game theory games in the quantum realm! View the source code on <a href="https://github.com/desireevl/quantum-game-theory">Github.</a></h4>
        <br />
        <br />
        <h5 style={{ textAlign: "center", fontSize: "16px"}}>Desiree Vogt-Lee, Kendrick Tan, Rajiv Krishnakumar, <br /> George Woodman, Severin Tschui, Jansen Zhao</h5>
        <br />
        <br />
        <br />
        <br />
        <div style={{textAlign: "center"}}>
          <Link to="/instructions">
            <Button color="link" style={{color: "#212529"}}>
              Start
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
