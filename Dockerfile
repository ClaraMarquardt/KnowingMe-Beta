# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         Dockerfile
# Purpose:      Build docker image - Production (Github Code)
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:        See the README for instructions on how to build the image

# ------------------------------------------------------------------------ #

# STAGE BASIC
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# Basic Setup (Ubuntu + Core dependencies incl. git, python, pip, postgresql)
# ------------------------------------------------------------------------ #

FROM ubuntu:latest  
RUN apt-get update  
RUN apt-get install --no-install-recommends --no-install-suggests -y --reinstall build-essential
RUN apt-get install --no-install-recommends --no-install-suggests -y g++-4.8 git bash python python-setuptools \
gcc python-pip libc-dev unixodbc-dev python-dev
RUN pip install --upgrade pip

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

RUN apt-get install -y openjdk-8-jre python-pycurl

# Info
# ------------------------------------------------------------------------ #
MAINTAINER Clara Marquardt "marquardt.clara@gmail.com”
RUN pwd
RUN ls root/

# Environment Variables
# ------------------------------------------------------------------------ #
ENV PORT 8000
ENV PORT_NLP 9000
ENV DEBUG "False"
ENV OFFLINE "False"

# Obtain Codebase (From Github)
# ------------------------------------------------------------------------ #
RUN git clone https://5f93c3a742abf9ec98d058391d49cb7970e90973:x-oauth-basic@github.com/ClaraMarquardt/KnowingMeBeta.git
RUN pwd

# Installation
# ------------------------------------------------------------------------ #

# Installation - Setup
# ---------------------------------------------
RUN pwd
WORKDIR /KnowingMeBeta/
RUN chmod -R a+rwx .

# Installation - Python Dependencies
# ---------------------------------------------

## Install Dependencies
RUN pip install --no-binary scipy scikit-learn  
RUN pip --no-cache-dir install -r codebase/requirements.txt           	   
RUN pip install --upgrade google-api-python-client        			           

## Test Dependencies
# RUN python codebase/installation/dependency_test.sh
RUN python codebase/installation/nltk_test.py  
RUN python codebase/installation/spacy_test.py  



# STAGE RESTARST
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

# Restart
# ---------------------------------------------
ARG RESTART=unknown
RUN RESTART=${RESTART} echo "stage_restart" # comment to restart here

# Reinstall codebase
# ---------------------------------------------
WORKDIR /
RUN pwd
RUN rm -rf /KnowingMeBeta

RUN git clone https://5f93c3a742abf9ec98d058391d49cb7970e90973:x-oauth-basic@github.com/ClaraMarquardt/KnowingMeBeta.git

WORKDIR /KnowingMeBeta/
RUN chmod -R a+rwx .

# Database Initialization
# ---------------------------------------------
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# Launch
# ---------------------------------------------
VOLUME /KnowingMe_Data
WORKDIR /KnowingMeBeta/
EXPOSE  $PORT
EXPOSE  $PORT_NLP
CMD ["/KnowingMeBeta/codebase/docker/docker_start.sh"]

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
