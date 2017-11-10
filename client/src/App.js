import React, { Component } from 'react';
import './App.css';

import {Layer, Rect, Text, Stage} from 'react-konva';
import PropTypes from 'prop-types';

export const CONSTANTS = {
  WEBSOCKET: "ws://"+window.location.host+"/websocket/gameview",
  CARD_WIDTH: 100,
  CARD_HEIGHT: 150,
  ACTIONS: {
    UPDATE: "UPDATE",
    OPTION: "OPTION"
  }
};

const SUITS = {
  YELLOW: '#FC0',
  BLUE: '#05F',
  RED: '#F00',
  PURPLE: '#F0C',
  BLACK: '#333'
};

class Card extends Component {

  render() {
    return (
      <span display="inline-block">
        <Stage width={CONSTANTS.CARD_WIDTH+10} height={CONSTANTS.CARD_HEIGHT+10} display="inline-block" >
          <Layer x={5} y={5}>
            <Rect
              width={CONSTANTS.CARD_WIDTH}
              height={CONSTANTS.CARD_HEIGHT}
              fill={this.props.suit}
              stroke={'#111'}
              strokeWidth={2}
              cornerRadius={2}
            />
            <Text
              text={this.props.text.charAt(0)}
              fontSize={80}
              fill={'#111'}
              width={CONSTANTS.CARD_WIDTH}
              padding={20}
              align={'center'}
            />
          </Layer>
        </Stage>
      </span>
    )
  }
}
Card.propTypes = {
  text: PropTypes.string,
  suit: PropTypes.string
};
Card.defaultProps = {
  text: '0', 
  suit: SUITS.YELLOW
};

// FIXME: enough of this export shit
export class GameSocketComponent extends Component {
  constructor(props) {
    super(props);
    const gameSocket = new WebSocket(CONSTANTS.WEBSOCKET);
    this.gameSocket = gameSocket;
    gameSocket.onmessage = (event) => {
      this.handleServerMessage(JSON.parse(event.data));
    };
  };

  handleServerMessage(data) {
    // check what action
    let action = data.action;
    delete data.action;
    switch (action) {
      case CONSTANTS.ACTIONS.UPDATE:
        this.props.updateUI(data)
        break;
      case CONSTANTS.ACTIONS.OPTION:
        this.props.displayTurn(data)
        break;
      default:
        console.log("action was not an expected value");
        break;
    }
  }

  sendMessage(data) {
    this.gameSocket.send(JSON.stringify(data));
  }

  render() {
    return (
      <div id="game_socket"/>
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
      top_card: {},
      card_actions: {}, // card.id -> action
    }
    this.gameSocketComponent = new GameSocketComponent({
      updateUI:this.handleUpdateUI.bind(this),
      displayTurn:this.handlePlayerTurn.bind(this)
    })
  };

  handleUpdateUI(data) {
    this.setState({
      hand: data.hand,
      top_card: data.top_card
    });
  }

  handlePlayerTurn(data) {
    // data is object id:action, id:action etc..
    var actions = {};
    Object.keys(data).forEach((key) => {
      let act = data[key];
      if (act.action !== "DRAW") {
        actions[act.card.id] = act;
      } else {
        this.setState({"drawCardAction": act});
      }
    });
    this.setState({
      card_actions: actions
    });
  }

  handlePlayCard(card_id) {
    // get the action related to the card_id
    this.sendInput(this.state.card_actions[card_id].id);
  }

  sendInput(value) {
    // send the input to the server, get rid of all the available actions
    this.gameSocketComponent.sendMessage({"input": value.toString()});
    this.setState({
      card_actions: {},
      drawCardAction: {}
    })
  }

  render() {
    let top_card_render = null;
    if (!(Object.keys(this.state.top_card).length === 0)) {
      top_card_render =
        <div id="top_card">
          <h2>Top Card</h2>
          <Card 
            text={this.state.top_card.value.toString()} 
            suit={SUITS[this.state.top_card.suit]}
          />
        </div>
    }
    const cards = this.state.hand.map((card, index) => 
      <span display="inline-block" key={card.id}>
        <Card 
          key={card.id} 
          text={card.value.toString()} 
          suit={SUITS[card.suit]}
        />
        {this.state.card_actions[card.id] && 
          <button href="#" onClick={this.handlePlayCard.bind(this, card.id)}>
            Play Card
          </button>
        }
      </span>
    );
    return (
      <div>
        {this.gameSocketComponent.render()}
        <div id="player_hand">
          <h2>Your hand</h2>
          <div className="container">
            {cards}
          </div>
        </div>
        {top_card_render}
        {this.state.drawCardAction && 
          <div>
            <Card 
              text=""
              suit={SUITS.BLACK}
            />
            <button href="#" onClick={this.sendInput.bind(this, this.state.drawCardAction.id)}>
              Draw
            </button>
          </div>
        }
      </div>
    );
  };
};

class App extends Component {
  render() {
    return (
      <div className="App">
        <Game />
      </div>
    );
  }
}

export default App;
