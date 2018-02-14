# Card Game

UNO, implemented in Python and ReactJS.

![game screenshot](readme_assets/game_screenshot1.png)

## Build Status
| Branch | Status |
| ------ | ------ |
| master | [![Build Status](https://travis-ci.org/JoelPagliuca/Card-Game.svg?branch=master)](https://travis-ci.org/JoelPagliuca/Card-Game) |
| dev    | [![Build Status](https://travis-ci.org/JoelPagliuca/Card-Game.svg?branch=dev)](https://travis-ci.org/JoelPagliuca/Card-Game) |

## Depencies
* `docker-compose`

## Running
`docker-compose up`

Game start page is [here](http://127.0.0.1:2180/#/start)

## Development
### Dependencies
* `docker`
* `virtualenv`
* `makefile` - optional (just read makefile for commands)
* `yarn` - optional (client can just be run through docker)

### Setup
`make dev`

### Unit tests
`make test`

### Solution structure
* 3 Docker containers
	* **client**
		* React front end
		* port 3000
	* **server**
		* Python-Tornado server
		* also mounts game logic code from `./card_game/`
		* port 8888
	* **proxy**
		* Nginx reverse for the other two containers
		* port 2180 
		* `/` maps to **client**:3000
		* `/websocket` maps to **server**:8888

* * *

## Directory
* card_game/
	* game logic - python code for the actual game implementation
* client/
	* client - react web app
* server/
	* server - python-tornado websocket
* test/
	* unit tests
* readme_assets/
	* content required for this README.md
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