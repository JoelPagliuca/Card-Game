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

  constructor(props) {
    super(props);
    this.state = {number_players: 3};
  }

  newGame() {
    var formData = new FormData();
    var number_players = this.state.number_players;
    formData.append("number_players", number_players);
    fetch(CONSTANTS.LOCATIONS.GAMECREATE, {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(json => {
      this.joinGame(json.game_id);
    });
  };

  joinGame(game_id) {
    this.props.history.push("/gameview/"+game_id);
  }

  render() {
    return (
      <Grid container spacing={24}>
        <Grid item xs={1}></Grid>
        <Grid item xs={5}>
          <Paper style={paper_style}>
            <h3>New Game</h3>
            <TextField
              onChange={this._handleNumPlayersChange.bind(this)}
              defaultValue="3"
              label="Number of players"
            />
            <Button raised color="primary" style={style} onClick={this.newGame.bind(this)}>Start</Button>
          </Paper>
        </Grid>
        <Grid item xs={5}>
          <Paper style={paper_style}>
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
  };

  _handleNumPlayersChange(element) {
    var value = element.target.value;
    this.setState({
      number_players: value
    });
  };
}

export default GameSelector;