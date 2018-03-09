#!/usr/bin/env bash

# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         docker_start
# Purpose:      Launch Docker Container
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Shell
# Notes:        See the README for instructions on how to build the image

# ------------------------------------------------------------------------ #

## Start nlp server
# java -mx4g -cp "codebase/dependencies/core_nlp/model/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -props codebase/dependencies/core_nlp/core_nlp.properties --port 9000 --timeout 10000

## Start postgresql
/etc/init.d/postgresql start

## Launch app
python /KnowingMe/codebase/KnowingMe.py

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
