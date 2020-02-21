import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom'
import { Button, Spinner } from 'reactstrap';
import FontAwesome from 'react-fontawesome'
import axios from 'axios'

const Results = (props) => {
  const { appState, setPlayerData } = props
  const { playerData } = appState
  const { protocolSelected, gameSelected, playersSelected, payoffMatrix, deviceSelected } = appState.settings
  const [data, setData] = useState(null)

  const toArray = (o) => {
    let arr = []

    let i = 0
    while (i in o) {
      if (Object.keys(o[i]).length > 0) {
        arr.push(o[i])
      }

      i++
    }

    return arr
  }

  useEffect(() => {
    const f = async () => {
      try {
        const { data } = await axios.post(
          'https://api-quantum-game.desireevl.com/',
          // 'http://127.0.0.1:5000/',
          {
            "protocol": protocolSelected,
            "game": gameSelected,
            "payoff": payoffMatrix,
            "players": playersSelected,
            "device": deviceSelected,
            "player1": toArray(playerData[0] || {}),
            "player2": toArray(playerData[1] || {}),
            "player3": toArray(playerData[2] || {}),
            "player4": toArray(playerData[3] || {}),
          }// 
// 
// 
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
  const playerDict = {"P1": "Player 1", "P2": "Player 2", "P3": "Player 3", "P4": "Player 4"}
  const circuitImg = data != null ? data["full_circ_str"]: null
  const graphImg = data != null ? data["graph_str"]: null

  console.log(appState)

  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
    <div style={{ textAlign: "center"}}>
      <h1 style={{ textAlign: "center"}}>Results</h1>
      <br />
      {
        graphImg === null ?
        (
          <Spinner animation="border" role="status">
            <span className="sr-only">Loading...</span>
          </Spinner>
        ) :
        (
          <>
            {
              winner != 'no winners' ?
              <h2>Congratulations to winner {playerDict[winner]}!</h2>:
              <h2>No winners :(</h2>
           }
           <hr />      
           <img src={`data:image/jpeg;base64,${encodeURIComponent(circuitImg)}`} width={"100%"}/>
           <img src={`data:image/png;base64,${encodeURIComponent(graphImg)}`} width={"60%"}/>
          </>
        )
        
      }

      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        <Link to="/">
          <Button  
          color="link" 
          style={{color: "#212529"}}
          onClick={() => {
            setPlayerData({})
          }}>
            Play Again
          </Button>
        </Link>
      </div>
    </div>
    </div>
  );
}

export default Results;
