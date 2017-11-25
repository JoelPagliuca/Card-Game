export const CONSTANTS = {
  CARD_WIDTH: 100,
  CARD_HEIGHT: 150,
};

export const LOCATIONS = {
  GAMEVIEW: "ws://"+window.location.host+"/websocket/gameview",
  GAMECREATE: "http://"+window.location.host+"/websocket/gamecreate"
}

export const ACTIONS = {
  UPDATE: "UPDATE",
  OPTION: "OPTION"
}

export const SUITS = {
  YELLOW: '#FC0',
  BLUE: '#05F',
  RED: '#F00',
  PURPLE: '#F0C',
  BLACK: '#333'
};