import React, { Component } from 'react';
import WebSocket from 'react-websocket';
import logo from './logo.svg';
import './App.css';

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

      <WebSocket url={"ws://"+window.location.host+"/websocket/hello"}
        onMessage={this.handleData.bind(this)} />
      
      </div>
    ); 
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
      </div>
    );
  }
}

export default App;
