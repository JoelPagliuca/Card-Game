import React, { Component } from 'react';
import WebSocket from 'react-websocket';
import logo from './logo.svg';
import './App.css';

import {Layer, Rect, Text, Stage} from 'react-konva';

const CONSTANTS = {
  WEBSOCKET: "ws://"+window.location.host+"/websocket/gameview"
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
      <Layer x={10} y={10}>
        <Rect
          width={100}
          height={150}
          fill={'#FC0'}
          stroke={'#111'}
          strokeWidth={2}
          cornerRadius={2}
        />
        <Text
          text={'8'}
          fontSize={80}
          fill={'#111'}
          width={100}
          padding={20}
          align={'center'}
        />
      </Layer>
    )
  }
}

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
          <Card />
        </Stage>
      </div>
    );
  }
}

export default App;
