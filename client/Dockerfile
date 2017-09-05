# with help from http://jdlm.info/articles/2016/03/06/lessons-building-node-app-docker.html
FROM node:6.11.2
RUN useradd --user-group --create-home --shell /bin/false app

ENV HOME=/home/app

COPY package.json yarn.lock $HOME/client/
RUN chown -R app:app $HOME/*

USER app
WORKDIR $HOME/client
RUN npm install