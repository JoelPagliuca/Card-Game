import React from 'react';
import ReactDOM from 'react-dom';
import { App, GameSocketComponent, CONSTANTS } from "./App";

// mock up the websocket
import { Server } from "mock-socket";

it('runs the SocketComponent?', () => {
  const mockServer = new Server(CONSTANTS.WEBSOCKET);
  mockServer.on('connection', (socket) => { // WHAT THE ACTUAL FUCK IS THIS socket VARIABLE FROM THE EXAMPLE?
    mockServer.send('{"action":"UPDATE"}');
  });
  const div = document.createElement('div');
  ReactDOM.render(<GameSocketComponent />, div);
  mockServer.listeners.connection[0](); // To actually run a connection, do this
});
