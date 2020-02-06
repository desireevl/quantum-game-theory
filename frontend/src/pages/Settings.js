import React, { useState } from 'react';

import { Link } from 'react-router-dom'
import { Button, ButtonToolbar, Modal, ModalHeader, ModalBody } from 'reactstrap';
import FontAwesome from 'react-fontawesome'

const InfoModal = (props) => {
  const { modal, setModal, title, content } = props

  const toggle = () => setModal(!modal);

  return (
    <div>
      <Modal centered isOpen={modal} toggle={toggle}>
        <ModalHeader toggle={toggle}>{title}</ModalHeader>
        <ModalBody>
          {content}
        </ModalBody>
      </Modal>
    </div>
  )
}

const Settings = (props) => {
  const { 
    appState, 
    setProtocolSelected,
    setGameSelected,
    setPlayersSelected,
    setPayoffSelected
  } = props
  const { settings } = appState
  const { gameSelected } = settings

  // Hide modal by default
  const [protocolModal, setProcotolModal] = useState(false)
  const [gameModal, setGameModal] = useState(false)


  return (
    <div style={{display: "flex", alignItems: "center", justifyContent: "center", height: "100vh"}}>
      <div style={{position: "fixed", top: 40, left: 50, width: "100%"}}>
      <Link to="/instructions">
        <FontAwesome className="fas fa-chevron-left" style={{color: "#212529"}}/>
      </Link>        
      </div>
      <div>
        <h1 style={{ textAlign: "center"}}>Settings</h1>
        <br />
          <h4>Protocol<Button color="link" onClick={() => setProcotolModal(true)}><FontAwesome className="fas fa-info-circle" style={{color: "#212529"}}/></Button></h4>
          <ButtonToolbar>
            <Button color="primary" onClick={() => setProtocolSelected('EWL')} active={settings.protocolSelected === 'EWL'}>EWL</Button>
            <Button color="primary" onClick={() => setProtocolSelected('MW')} active={settings.protocolSelected === 'MW'}>MW</Button>
          </ButtonToolbar>
          <br />

          <h4>Game<Button color="link" onClick={() => setGameModal(true)}><FontAwesome className="fas fa-info-circle" style={{color: "#212529"}}/></Button></h4>
          <ButtonToolbar>
            <Button color="primary" onClick={() => setGameSelected('prisoner')} active={settings.gameSelected === 'prisoner'}>Prisoners</Button>
            <Button color="primary" onClick={() => setGameSelected('minority')} active={settings.gameSelected === 'minority'}>Minority</Button>
            <Button color="primary" onClick={() => {
              setGameSelected('chicken')
              setPlayersSelected(2)
            }} active={settings.gameSelected === 'chicken'}>Chicken</Button>
            <Button color="primary" onClick={() => {
              setGameSelected('BoS')
              setPlayersSelected(2)
            }} active={settings.gameSelected === 'BoS'}>BoS</Button>
          </ButtonToolbar>
          <br />

          <h4>Players</h4>
          <ButtonToolbar>
            <Button color="primary" onClick={() => setPlayersSelected(2)} active={settings.playersSelected === 2}>2</Button>
            <Button 
              disabled={gameSelected === "chicken" || gameSelected === "BoS"}
              color="primary" onClick={() => setPlayersSelected(3)} active={settings.playersSelected === 3}>3</Button>
            <Button
              disabled={gameSelected === "chicken" || gameSelected === "BoS"}
              color="primary" onClick={() => setPlayersSelected(4)} active={settings.playersSelected === 4}>4</Button>
          </ButtonToolbar>
          <br />

          {/* <h4>Payoff</h4>
          <ButtonToolbar>
            <Button color="primary" onClick={() => setPayoffSelected('Defined')} active={settings.payoffSelected === 'Defined'}>Defined</Button>
            <Button color="primary" onClick={() => setPayoffSelected('Custom')} active={settings.payoffSelected === 'Custom'}>Custom</Button>
          </ButtonToolbar> */}

        <br />
        <br />
        <br />
        <br />
        <div style={{textAlign: "center"}}>
          <Link to="/player">
            <Button color="link" style={{color: "#212529"}}>
              Play
            </Button>
          </Link>
        </div>
      </div>

      <InfoModal
        modal={protocolModal}
        setModal={setProcotolModal}
        title={"Protocol"}
        content={(<div>A protocol is a method to convert a classical game to a quantum game. A quantum protocol needs to one, distribute maximally entangled qubits to the players, and two, generalise the classical version of the game. There are two protocols implemented here: 
          <ul>
            <li style={{fontSize: "16px"}}>EWL protocol: The first quantum game theory protocol invented by <a href="https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.83.3077">Eisert, Wilkens & Lewenstein</a> utilising a J operator entangling gate to create a superposition between players and J&#8224; disentangling operator</li>
            <li style={{fontSize: "16px"}}>MW protocol: A secondary protocol created by <a href="https://arxiv.org/abs/quant-ph/0004081">Marinatto and Weber</a> with the only difference to the EWL protocol being the absence of the disentangling gate</li>
          </ul>
          <a href="https://link.springer.com/article/10.1007/s11128-018-2082-8">Khan et al (2018)</a> has a comprehensive review on quantum protocols.</div>)}
      />
      <InfoModal
        modal={gameModal}
        setModal={setGameModal}
        title={"Game"}
        content={(<div>
          <ul>
            <li style={{fontSize: "16px"}}><a href="https://en.wikipedia.org/wiki/Prisoner%27s_dilemma">Prisoner's Dilemma</a>: All players are involved in committing a crime and get caught, but not quite red handed. In order to get a confession from all players, the police separate each player into different rooms and present two options: one, to remain silent, and two, to confess and maybe receive a reduced sentence.</li>
            <li style={{fontSize: "16px"}}><a href="https://en.wikipedia.org/wiki/El_Farol_Bar_problem">Minority Game</a>: A simple game in which a player wins the game if their outcome is different to everyone else's.</li>
            <li style={{fontSize: "16px"}}><a href="https://en.wikipedia.org/wiki/Chicken_(game)">Chicken Game</a>: Two players are heading towards each other. If the players both continue on the same path, they collide with each other. If one swerves out of the way and the other doesn't, the swerver loses and is labelled the chicken, while the other, implicitly braver player, wins.</li>
            <li style={{fontSize: "16px"}}><a href="https://en.wikipedia.org/wiki/Battle_of_the_sexes_(game_theory)">Bach or Stravinksy</a>: Two player want to go to concert together. One player prefers Bach and the other Stravinksy, however they would both prefer to attend a concert together than alone.</li>
          </ul>
          </div>)}
      />
    </div>
  );
}

export default Settings;
