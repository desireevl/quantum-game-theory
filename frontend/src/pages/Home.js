import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';

const Home = () => {
  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div>
        <h1 style={{ textAlign: "center"}}>Quantum Game Theory</h1>
        <br />
        <h5 style={{ textAlign: "center"}}>Rajiv Krishnakumar, Kendrick Tan, Severin Tschui, <br /> Desiree Vogt-Lee, George Woodman, Jansen Zhao</h5>
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
