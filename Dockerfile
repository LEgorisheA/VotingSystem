FROM python:3.11-slim AS build_env

# get master branch
COPY . /VotingSystem/
WORKDIR /VotingSystem/

RUN pip3 install --no-cache-dir -r requirements.txt

# create no-root users for run server
RUN groupadd runner && useradd -g runner runner

CMD su runner &&\
    gunicorn -w 4 --bind 0.0.0.0:5000 "app.main:create_app()"