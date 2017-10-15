import React, { Component } from 'react';
import WebSocket from 'react-websocket';
import logo from './logo.svg';
import './App.css';

import {Layer, Rect, Text, Stage} from 'react-konva';

const CONSTANTS = {
  WEBSOCKET: "ws://"+window.location.host+"/websocket/gameview",
  CARD_WIDTH: 100
}

const SUITS = {
  YELLOW: '#FC0',
  BLUE: '#05F',
  RED: '#F00',
  PURPLE: '#F0C'
}

class SocketComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: ""
    };
  }

  handleData(data) {
    let result = JSON.stringify(data);
    this.setState({data: result});
  }

  render() {
    return (
      <div><h3>Here is the WebSocket content:</h3>
      {this.state.data}

      <WebSocket url={CONSTANTS.WEBSOCKET}
        onMessage={this.handleData.bind(this)} />
      
      </div>
    ); 
  }
}

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
  text: React.PropTypes.string,
  suit: React.PropTypes.string,
  x: React.PropTypes.number,
  y: React.PropTypes.number
};
Card.defaultProps = { 
  text: '0', 
  suit: SUITS.YELLOW,
  x: 10,
  y: 10
};

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <SocketComponent />
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
