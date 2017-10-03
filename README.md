# Card Game

Python code for playing card games. Not a heap of functionality so far.

## Build Status
| Branch | Status |
| ------ | ------ |
| master | [![Build Status](https://travis-ci.org/JoelPagliuca/Card-Game.svg?branch=master)](https://travis-ci.org/JoelPagliuca/Card-Game) |
| dev    | [![Build Status](https://travis-ci.org/JoelPagliuca/Card-Game.svg?branch=dev)](https://travis-ci.org/JoelPagliuca/Card-Game) |

## Depencies
* `python2`

## Running
`python main.py`

## Development
### Dependencies
* `virtualenv`
* `makefile` - optional

### Setup
`make dev`

### Unit tests
`make test`

* * *

## Directory
* card_game/
	* python code for the actual game implementation
* client/
	* react web app for the players
* server/
	* python-tornado websocket server
* test/
	* unit tests
* .gitignore
* .travis.yml
	* travis build config
* README.md
	* this file
* TIL.md
	* stuff I learnt while working on this project
* docker-compose.yml
	* Docker configuration for this project
* main.py
	* manual tests for the card-game code
* makefile
	* simple automation tasks using make
* nginx.conf
	* config for the nginx reverse proxy
* setup.cfg
	* settings for the python card-game code

Any other files that pop up are automatically generated.