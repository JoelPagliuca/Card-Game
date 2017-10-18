import React from 'react';
import ReactDOM from 'react-dom';
import { App, GameSocketComponent, CONSTANTS } from "./App";
import { shallow } from "enzyme";
import sinon from "sinon";

// mock up the websocket
import { Server } from "mock-socket";

describe("GameSocketCompoent", () => {
  
  // mock for websocket server
  var mockServer = new Server(CONSTANTS.WEBSOCKET);
  mockServer.on('connection', (socket) => { // WHAT THE ACTUAL FUCK IS THIS socket VARIABLE FROM THE EXAMPLE?
    mockServer.send('{"action":"UPDATE", "top_card":{"value":"6", "suit":"RED"}}');
  });
  // mocks for functions
  let nothingStub = sinon.stub();
  let updateStub = sinon.stub();
  let optionsStub = sinon.stub();
  
  
  it('runs without crashing', () => {
    let component = shallow(<GameSocketComponent updateUI={nothingStub}/>);
    expect(component).toBeDefined();
  });
  
  it('runs the update function', () => {
    shallow(<GameSocketComponent updateUI={updateStub}/>);
    mockServer.listeners.connection[0](); // To actually run a connection, do this
    sinon.assert.calledOnce(updateStub);
  });
  
  afterEach(() => {
    console.log(updateStub.callCount)
    updateStub.reset();
  });
});
