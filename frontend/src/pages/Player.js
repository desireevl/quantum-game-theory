import React, { useState } from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const Player = (props) => {
  const [curPlayerNo, setCurPlayerNo] = useState(1)

  const { appState, setPlayerData } = props
  const { settings, playerData } = appState

  const testData = {
    playerNo: curPlayerNo
  }

  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: "5%", width: "100%"}}>
      <Link to="/settings">
        <FontAwesome className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
      <div style={{position: "fixed", top: 40, left: "95%", width: "100%"}}>
      <Link to="/settings">
        <FontAwesome className="fas fa-cog fa-lg" style={{color: "#212529"}}/>
      </Link>        
      </div>
    <div>
      <h1 style={{ textAlign: "center"}}>Player { curPlayerNo }</h1>
      <br />
      Test
      <br />
      <br />
      <br />
      <br />
      <div style={{textAlign: "center"}}>
        {
          curPlayerNo === settings.playersSelected ?
          (
            <Link to="/results">
              <Button color="link" style={{color: "#212529"}}>
                Next
              </Button>
            </Link>
          ) :
          (
            <Button
              color="link"
              style={{color: "#212529"}}
              onClick={() => {
                let newPlayerData = playerData
                newPlayerData[curPlayerNo] = testData // TODO: replace test data with your real data

                setPlayerData(newPlayerData)
                setCurPlayerNo(curPlayerNo + 1)
              }}
            >
              Next
            </Button>
          )
        }
      </div>
    </div>
    </div>
  );
}

export default Player;