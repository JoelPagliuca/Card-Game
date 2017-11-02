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
    let action = data.action;
    delete data.action;
    switch (action) {
      case "UPDATE":
        this.props.updateUI(data)
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

/**
 * responsible for rendering the player's view of the game
 * mostly the hand
 */
class Game extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      hand: [],
      top_card: {}
    }
  };

  handleUpdateUI(data) {
    this.setState({
      hand: data.hand,
      top_card: data.top_card
    });
  }

  render() {
    return (
      <div>
        <GameSocketComponent
          updateUI={this.handleUpdateUI.bind(this)}
        />
        <h2>Your hand</h2>
        <Stage className="Player-hand" width={1000} height={200}>
          { this.state.hand.map((card, index) => {
            return new Card({
              text: card.value.toString(), 
              suit: SUITS[card.suit], 
              x: 10+(index*(CONSTANTS.CARD_WIDTH+10)),
              y: 10
            }).render();
          }) }
        </Stage>
        <h2>Top Card</h2>
        <Stage className="Top-card" width={250} height={200}>
          { new Card({
            text: this.state.top_card.value.toString(),
            suit: SUITS[this.state.top_card.suit],
            x: 10,
            y: 10
          }).render() }
        </Stage>
      </div>
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
      </div>
    );
  }
}

export default App;
