FROM python:3.11-slim AS build_env

# install requirements
COPY requirements.txt /VotingSystem/
WORKDIR /VotingSystem/
RUN pip install -r requirements.txt

# copy master branch
WORKDIR /VotingSystem/
COPY . /VotingSystem/

# create no-root users for run server
RUN groupadd runner && useradd -g runner runner

ENV PYTHONPATH ${PYTHONPATH}:/hope-project/app/
CMD su runner && \
    gunicorn --workers=8 --bind=webapp:5000 "app.main:create_app()"