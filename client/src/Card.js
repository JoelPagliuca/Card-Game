import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {Layer, Rect, Text, Stage} from 'react-konva';
import Grid from 'material-ui/Grid';
import Button from 'material-ui/Button';

import { CARD_PROPS, SUITS } from "./Constants";

export class Card extends Component {

  render() {
    return <Grid item>
      <Stage width={CARD_PROPS.CARD_WIDTH+10} height={CARD_PROPS.CARD_HEIGHT+10}>
        <Layer x={5} y={5}>
          <Rect
            width={CARD_PROPS.CARD_WIDTH}
            height={CARD_PROPS.CARD_HEIGHT}
            fill={this.props.suit}
            stroke={'#111'}
            strokeWidth={2}
            cornerRadius={2}
          />
          <Text
            text={this.props.text.charAt(0)}
            fontSize={CARD_PROPS.CARD_TEXT_SIZE}
            fill={'#111'}
            width={CARD_PROPS.CARD_WIDTH}
            padding={20}
            align={'center'}
          />
        </Layer>
      </Stage>
    </Grid>
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

class Action extends Component {
  /** 
   * turns an JSON action into a button
   * this.handlePlayCard.bind(this, card.id)
   */
  render() {
    return <Button raised color="primary" onClick={this.props.callback.bind(this, this.props.action.id)}>
      {this.props.action.action}
    </Button>
  }
}

export class ActionGroup extends Component {
  // a group of actions, given as an array of JSON arrays
  render () {
    console.log(this.props.callback)
    var actionComponents = this.props.actions.map((act) => {
      return <Grid item xs={12} key={act.id}>
        <Action action={act} callback={this.props.callback}></Action>
      </Grid>
    });
    return <Grid container>
      {actionComponents}
    </Grid>
  }
}

export class CardWithActions extends Component {
  /**
   * card + actions
   */
  render () {
    const card = this.props.card;
    return 
    
    <Card 
      key={card.id} 
      text={card.value.toString()} 
      suit={SUITS[card.suit]}
    />
  }
}