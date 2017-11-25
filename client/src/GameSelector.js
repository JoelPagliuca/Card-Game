import React, { Component } from 'react';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import Paper from 'material-ui/Paper';
import Grid from 'material-ui/Grid';

import * as CONSTANTS from './Constants'

const style = { // FIXME obviously not in the right spot
  margin: 12
}

/**
 * First point of contact, user -> new game or join game
 */
const paper_style = {
  padding: 6
}
class GameSelector extends Component {

  newGame() {
    var formData = new FormData();
    formData.append("number_players", this.refs.numberPlayers.getValue());
    fetch(CONSTANTS.LOCATIONS.GAMECREATE, {
      method: "POST",
      body: formData
    });
  };

  joinGame(game_id) {
    
  }

  render() {
    return (
      <Grid container spacing="24">
        <Grid item xs={1}></Grid>
        <Grid item xs={5}>
          <Paper zDepth="2" style={paper_style}>
            <h3>New Game</h3>
            <TextField
              ref="numberPlayers"
              defaultValue="3"
              label="Number of players"
            />
            <Button raised color="primary" style={style} onClick={this.newGame}>Start</Button>
          </Paper>
        </Grid>
        <Grid item xs={5}>
          <Paper zDepth="2" style={paper_style}>
            <h3>Join Game</h3>
            <TextField
              label="Game ID"
            />
            <Button raised color="primary" style={style}>Join</Button>
          </Paper>
        </Grid>
        <Grid item xs={1}></Grid>
      </Grid>
    );
  }
}

export default GameSelector;