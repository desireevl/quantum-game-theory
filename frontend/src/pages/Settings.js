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
            }} active={settings.gameSelected === 'BoS'}>Bos</Button>
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
        content={"The quantum protocol follows two rules: <h1>test</h1>"}
      />
      <InfoModal
        modal={gameModal}
        setModal={setGameModal}
        title={"Game"}
        content={"Ok thi s is some content"}
      />
    </div>
  );
}

export default Settings;