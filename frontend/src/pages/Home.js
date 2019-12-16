import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';

const Home = () => {
  return (
    <div>
      Home <br />

      <Link to="/instructions">
        <Button color="primary">
          Goto instructions
        </Button>
      </Link>
    </div>
  );
}

export default Home;
