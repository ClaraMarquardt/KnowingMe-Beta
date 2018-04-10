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

## Start postgresql
/etc/init.d/postgresql start

## Launch app
python /KnowingMeBeta/codebase/KnowingMe.py

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
