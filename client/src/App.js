import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import {Layer, Rect, Text, Stage} from 'react-konva';
import PropTypes from 'prop-types';

export const CONSTANTS = {
  WEBSOCKET: "ws://"+window.location.host+"/websocket/gameview",
  CARD_WIDTH: 100,
  ACTIONS: {
    UPDATE: "UPDATE",
    OPTION: "OPTION"
  }
};

const SUITS = {
  YELLOW: '#FC0',
  BLUE: '#05F',
  RED: '#F00',
  PURPLE: '#F0C'
};

class Card extends Component {

  render() {
    return (
      <Layer x={this.props.x} y={this.props.y}>
        <Rect
          width={CONSTANTS.CARD_WIDTH}
          height={150}
          fill={this.props.suit}
          stroke={'#111'}
          strokeWidth={2}
          cornerRadius={2}
        />
        <Text
          text={this.props.text}
          fontSize={80}
          fill={'#111'}
          width={CONSTANTS.CARD_WIDTH}
          padding={20}
          align={'center'}
        />
      </Layer>
    )
  }
}
Card.propTypes = {
  text: PropTypes.string,
  suit: PropTypes.string,
  x: PropTypes.number,
  y: PropTypes.number
};
Card.defaultProps = { 
  text: '0', 
  suit: SUITS.YELLOW,
  x: 10,
  y: 10
};

// FIXME: enough of this export shit
export class GameSocketComponent extends Component {
  constructor(props) {
    super(props);
    const gameSocket = new WebSocket(CONSTANTS.WEBSOCKET);
    gameSocket.onmessage = (event) => {
      this.handleServerMessage(JSON.parse(event.data));
    };
  };

  handleServerMessage(data) {
    // check what action
    switch (data.action) {
      case "UPDATE":
        console.log("UPDATE");
        break;
      case CONSTANTS.ACTIONS.OPTION:
        console.log("OPTIONS");
        break;
      default:
        console.log("action was not an expected value");
        break;
    }
  }

  render() {
    return (
      <div/>
    ); 
  }
}

class Game extends Component {
  
  constructor(props) {
    super(props);
  };

  render() {
    return (
      <GameSocketComponent
     />
    );
  };
};

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <Game />
        <Stage width={700} height={700}>
          <Card text={'8'} suit={SUITS.BLUE}/>
          <Card text={'4'} suit={SUITS.PURPLE} x={CONSTANTS.CARD_WIDTH+10+10}/>
          <Card text={'R'} suit={SUITS.YELLOW} x={2*(CONSTANTS.CARD_WIDTH+10)+10}/>
          <Card text={'0'} suit={SUITS.RED} x={3*(CONSTANTS.CARD_WIDTH+10)+10}/>
        </Stage>
      </div>
    );
  }
}

export default App;
