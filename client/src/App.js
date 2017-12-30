import React, { Component } from 'react';
import './App.css';

import {Layer, Rect, Text, Stage} from 'react-konva';
import PropTypes from 'prop-types';
import { HashRouter, Route } from 'react-router-dom'

import { MuiThemeProvider, createMuiTheme } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Grid from 'material-ui/Grid';

import GameSelector from './GameSelector'

// FIXME duplication
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

const theme = createMuiTheme();

class Card extends Component {

  render() {
    return (
      <Grid item>
        <Stage width={CONSTANTS.CARD_WIDTH+10} height={CONSTANTS.CARD_HEIGHT+10}>
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
      </Grid>
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
    const gameSocket = new WebSocket(CONSTANTS.WEBSOCKET + "/" + props.game_id);
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
      game_id: this.props.match.params.game_id,
      hand: [],
      top_card: {},
      card_actions: {}, // card.id -> action
    }
    this.gameSocketComponent = new GameSocketComponent({
      updateUI: this.handleUpdateUI.bind(this),
      displayTurn: this.handlePlayerTurn.bind(this),
      game_id: this.state.game_id
    })
  };

  handleUpdateUI(data) {
    this.setState({
      hand: data.hand,
      top_card: data.top_card,
      current_player: data.current_player,
      players: data.players
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
        <Grid item xm={6} id="top_card">
          <Card 
            text={this.state.top_card.value.toString()} 
            suit={SUITS[this.state.top_card.suit]}
          />
        </Grid>
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
      <Grid container spacing={24}>
        {this.gameSocketComponent.render()}
        <Grid container item xs={4}>
          {top_card_render}
          {this.state.drawCardAction && 
            <Grid item xs={6}>
              <Card 
                text=""
                suit={SUITS.BLACK}
              />
              <button href="#" onClick={this.sendInput.bind(this, this.state.drawCardAction.id)}>
                Draw
              </button>
            </Grid>
          }
        </Grid>
        <Grid item xs={8}>
          <h2>State</h2>
          { this.state.players && <b>Players:<br/></b>}
          { this.state.players && this.state.players.map((player, index) =>
            <span key={player.id}>
              <span>{player.name}</span><br/>
              <span> {player.num_cards} cards</span><br/>
            </span>
            ) }
          <span><b>Current player:</b> { this.state.current_player && this.state.current_player.name }</span>
        </Grid>
        <Grid item xs={12} id="player_hand">
          <h2>Your hand</h2>
          <Grid container>
            {cards}
          </Grid>
        </Grid>
      </Grid>
    );
  };
};



class App extends Component {
  render() {
    return (
      <MuiThemeProvider theme={theme}>
        <div className="App">
          <AppBar position="static">
            <Toolbar>
              <Typography type="title" color="inherit">
                UNO
              </Typography>
            </Toolbar>
          </AppBar>
          <HashRouter>
            <div id="content">
              <Route path="/start" component={GameSelector} />
              <Route path="/gameview/:game_id" component={Game} />
            </div>
          </HashRouter>
          {/* <Game /> */}
        </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
