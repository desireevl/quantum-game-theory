import React, { useState } from 'react';

import { Link } from 'react-router-dom'
import { Button } from 'reactstrap';
import { useDrag, useDrop } from 'react-dnd'
import Backend from 'react-dnd-html5-backend'
import FontAwesome from 'react-fontawesome'
import { DndProvider } from 'react-dnd'

const ItemTypes = {
  Gate: 'gate',
}

const Gate = ({ name, color }) => {
  const gateStyle = {
    border: '1px gray',
    backgroundColor: color,
    padding: '0.5rem 1rem',
    marginRight: '1.25rem',
    marginBottom: '1.25rem',
    cursor: 'move',
    float: 'left',
  }

  const [{ isDragging }, drag] = useDrag({
    item: { name, color, type: ItemTypes.Gate },
    end: (item, monitor) => {
      const dropResult = monitor.getDropResult()
      if (item && dropResult) {
      }
    },
    collect: monitor => ({
      isDragging: monitor.isDragging(),
    }),
  })
  const opacity = isDragging ? 0.4 : 1
  return (
    <div ref={drag} style={{ ...gateStyle, opacity }}>
      {name}
    </div>
  )
}

const GateNode = ({ 
  curPlayerIndex,
  playerGateData,
  playerIndex,
  gateIndex,
  setCurGateNo,
  curGateNo,
  setPlayerGateData
}) => {
  const gateNodeStyle = {
    height: '1rem',
    marginRight: '1.25rem',
    marginBottom: '1.25rem',
    padding: '1rem',
    textAlign: 'center',
    fontSize: '1rem',
    lineHeight: 'normal',
    float: 'left',
    zIndex: 1
  }

  const [gate, setGate] = useState(null)

  const [{ canDrop, isOver }, drop] = useDrop({
    accept: ItemTypes.Gate,
    drop: (x) => {
      if (curPlayerIndex === playerIndex && gateIndex <= curGateNo) {
        setGate(x)

        if (gateIndex === curGateNo) {
          setCurGateNo(curGateNo + 1)
        } else {
          setCurGateNo(curGateNo)
        }

        setPlayerGateData(x.name)
      }
    },
    collect: monitor => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop() && curPlayerIndex === playerIndex && gateIndex <= curGateNo,
    }),
  })

  let backgroundColor = 'inherit'
  let border = '1px solid rgba(0,0,0,0)' // have this here so px border is consistent
  let text = ''

  const cp = playerGateData[curPlayerIndex] || {}
  const cpg = cp[gateIndex]
  if (gate !== null && curPlayerIndex === playerIndex && cpg !== undefined && cpg !== null) {
    text = gate.name
    backgroundColor = gate.color
    border = '1px solid black'
  }

  if (canDrop && isOver) {
    backgroundColor = 'grey'
    border = '1px solid black'
  } else if (canDrop) {
    backgroundColor = 'white'
    border = '1px solid grey'
  }

  return (
    <div ref={drop} style={{ ...gateNodeStyle, backgroundColor, border }}>
      <span style={{ position: 'relative', top: '-0.6em'}}>{ text }</span>
    </div>
  )
}


const Player = (props) => {
  const [curPlayerNo, setCurPlayerNo] = useState(1)
  const [curGateNo, setCurGateNo] = useState(0)
  const [playerGateData, setPlayerGateData] = useState({
    0: {},
    1: {},
    2: {},
    3: {}
  })

  const { appState, setPlayerData } = props
  const { settings, playerData } = appState

  const gates = [
    { name: 'X', color: '#d3f6f3' },
    { name: 'Y', color: '#f9fce1' },
    { name: 'Z', color: '#fee9b2' },
    { name: 'H', color: '#fbd1b7' },
    { name: 'S', color: '#f1c6e7' },
    { name: 'T', color: '#e0f5b9' },
    { name: 'I', color: '#fddede' },
    { name: 'Rz1', color: '#fffbbe' },
    { name: 'Rz2', color: '#dfd3c3' },
    { name: 'Ry1', color: '#deecff' },
    { name: 'W', color: '#d4a5a5' },
  ]

  const gateNodeNo = 8

  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: "5%", width: "100%"}}>
      <Link to="/settings">
        <FontAwesome name="back" className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
      <div style={{position: "fixed", top: 40, left: "95%", width: "100%"}}>
      <Link to="/settings">
        <FontAwesome name="settings" className="fas fa-cog fa-lg" style={{color: "#212529"}}/>
      </Link>        
      </div>
    <div style={{ textAlign: 'center' }}>
      <h1>Player { curPlayerNo }</h1>
      <br />
      <h4 align='left'>Gates</h4>
      <br />

      <div style={{ width: '750px' }}>
        <DndProvider backend={Backend} style={{ textAlign: 'center', width: '100%' }}>
          <div style={{ clear: 'both', marginLeft: '1.2em' }}>
            {
              gates.map(g => <Gate key={g.name} name={g.name} color={g.color} />)
            }
          </div>
          <br />
          <br />
          <br />
          <br />
          <br />
          {
            Array(settings.playersSelected).fill(0).map((_, playerIdx) => (
              <div key={playerIdx} style={{ clear: 'both' }}>
                <div
                  style={{ zIndex: -1, position: 'relative', left: '2.25em', top: '1em', width: '700px', borderBottom: '1px solid black' }}
                >
                </div>
                <div style={{ float: 'left', fontFamily: 'monospace', fontSize: '20px' }}>
                  <strong>|0 &gt;</strong>
                </div>
                <div style={{ paddingLeft: '4em', width: '700px' }}>
                  {
                    Array(gateNodeNo)
                      .fill(0)
                      .map((_, gateIdx) => {
                        return <GateNode
                          key={gateIdx}
                          playerGateData={playerGateData}
                          curPlayerIndex={curPlayerNo - 1}
                          playerIndex={playerIdx}
                          gateIndex={gateIdx}
                          curGateNo={curGateNo}
                          setCurGateNo={setCurGateNo}
                          setPlayerGateData={(g) => {
                            let newPlayerGateData = playerGateData

                            if (newPlayerGateData[curPlayerNo - 1] === undefined) {
                              newPlayerGateData[curPlayerNo - 1] = {}
                            }

                            newPlayerGateData[curPlayerNo - 1][curGateNo] = g

                            setPlayerGateData(newPlayerGateData)
                          }}
                        />
                      })
                  }
                </div>
              </div>
            ))
          }
          </DndProvider>
      </div>

      <br />
      <br />
      <br />

      <div style={{textAlign: 'center'}}>
        <Button
          color="link"
          style={{ fontSize: '12px', color: "#212529"}}
          onClick={() => {
            let newPlayerData = Object.assign({}, playerData)
            newPlayerData[curPlayerNo - 1] = {}

            setPlayerGateData(newPlayerData)
            setCurGateNo(0)
          }}
        >
          Clear All
        </Button>
      </div>
      <br />
      <div style={{textAlign: "center"}}>
        {
          curPlayerNo === settings.playersSelected ?
          (
            <Link to="/results">
              <Button
                color="link"
                style={{color: "#212529"}}
                onClick={() => {
                  let newPlayerData = playerData
                  newPlayerData[curPlayerNo - 1] = playerGateData[curPlayerNo - 1]

                  setPlayerData(newPlayerData)
                  setCurPlayerNo(curPlayerNo + 1)
                  setCurGateNo(0)
                }}
              >
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
                newPlayerData[curPlayerNo - 1] = playerGateData[curPlayerNo - 1]

                setPlayerData(newPlayerData)
                setCurPlayerNo(curPlayerNo + 1)
                setCurGateNo(0)
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
