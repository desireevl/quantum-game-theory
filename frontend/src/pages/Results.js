import React from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'
import axios from 'axios'

const Results = ({ appState }) => {
  console.log(appState)

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
          <Button
            color="link"
            style={{color: "#212529"}}
            onClick={() => {
              const f = async () => {
                try {
                  const { data } = await axios.post(
                    'https://api-quantum-game.desireevl.com/',
                    {
                      "protocol": "EWL",
                      "game": "4-minority",
                      "payoff": null,
                      "players": 4,
                      "player1": ["X", "Y"],
                      "player2": ["X", "S"],
                      "player3": ["X", "S"],
                      "player4": ["X", "S"]
                    }
                  )

                  console.log(data)
                } catch (e) {
                  console.log(`${e}`)
                }
              }
              
              f()
            }}
          >
            Play Again
          </Button>
      </div>
    </div>
    </div>
  );
}

export default Results;
