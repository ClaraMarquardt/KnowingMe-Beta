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
RUN apt-get update && apt-get install -my wget gnupg
RUN apt-get install --no-install-recommends --no-install-suggests -y --reinstall build-essential
RUN apt-get install --no-install-recommends --no-install-suggests -y g++-4.8 git bash python python-setuptools \
gcc python-pip libc-dev unixodbc-dev python-dev
RUN pip install --upgrade pip

RUN apt-get install -y openjdk-8-jre python-pycurl

# Info
# ------------------------------------------------------------------------ #
MAINTAINER Clara Marquardt "marquardt.clara@gmail.com”
RUN pwd
RUN ls root/

# Environment Variables
# ------------------------------------------------------------------------ #
ENV PORT 8000
ENV DEBUG "False"
ENV OFFLINE "False"
ENV TIMEZONE_OFFSET 4
ENV TIMEZONE_NAME "EST"
ENV SAFE_MODE "False"

# Obtain Codebase (From Github)
# ------------------------------------------------------------------------ #
RUN git clone https://5f93c3a742abf9ec98d058391d49cb7970e90973:x-oauth-basic@github.com/ClaraMarquardt/KnowingMeBeta_Test.git
RUN pwd

# Installation
# ------------------------------------------------------------------------ #

# Installation - Setup
# ---------------------------------------------
RUN pwd
WORKDIR /KnowingMeBeta_Test/
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


# STAGE RESTART
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
RUN rm -rf /KnowingMeBeta_Test

RUN git clone https://5f93c3a742abf9ec98d058391d49cb7970e90973:x-oauth-basic@github.com/ClaraMarquardt/KnowingMeBeta_Test.git

WORKDIR /KnowingMeBeta_Test/
RUN chmod -R a+rwx .

# Launch
# ---------------------------------------------
VOLUME /KnowingMe_Data
WORKDIR /KnowingMeBeta_Test/
EXPOSE  $PORT
CMD ["/KnowingMeBeta_Test/codebase/docker/docker_start.sh"]

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
