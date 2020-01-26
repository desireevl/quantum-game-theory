import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'
import axios from 'axios'

const Results = (props) => {
  const { appState } = props
  const { protocolSelected, gameSelected, playersSelected } = appState.settings
  const [data, setData] = useState(null)

  useEffect(() => {
    const f = async () => {
      try {
        const { data } = await axios.post(
          'https://api-quantum-game.desireevl.com/',
          // 'http://127.0.0.1:5000/',
          {
            "protocol": protocolSelected,
            "game": gameSelected,
            "payoff": null,
            "players": playersSelected,
            "player1": ["X", "Y"],
            "player2": ["X", "Y"],
            "player3": ["X", "S"],
            "player4": ["X", "S"]
          }
        )
        setData(data)
        console.log(data)
      } catch (e) {
        console.log(`${e}`)
      }
    }

    if (data === null) {
      f()
    }
  })

  const numPlayers = data != null ? data["players"] : null
  const winner = data != null ? data["winners"]: []
  const winnerNum = data != null ? (data["winners"].length > 1 ? "winners": "winner"): null
  const playerDict = {"P1": "Player 1", "P2": "Player 2", "P3": "Player 3", "P4": "Player 4"}
  const circuitImg = data != null ? data["full_circ_str"]: null
  const graphImg = data != null ? data["graph_str"]: null


  console.log(appState)

  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
    <div style={{ textAlign: "center"}}>
      <h1 style={{ textAlign: "center"}}>Results</h1>
      <br />
      <h4>Congratulations to {winnerNum} {playerDict[winner]}!</h4>

      {/* {data["winners"].length != 0 ? "No winners": "Congrats to winner"} */}

      <h4>Probability graph</h4>
      <img src={`data:image/png;base64,${encodeURIComponent(graphImg)}`} width={"60%"}/>

      <h4>Full circuit for {numPlayers} players</h4>
      <img src={`data:image/jpeg;base64,${encodeURIComponent(circuitImg)}`} width={"100%"}/>

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

export default Results;