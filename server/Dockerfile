FROM python:2.7.13

RUN useradd --user-group --create-home --shell /bin/false app

ENV HOME=/home/app

COPY requirements.txt $HOME/server/
# RUN chown -R app:app $HOME/*

# USER app
WORKDIR $HOME/server
RUN pip install -r requirements.txt