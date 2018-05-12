# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         Manual
# Purpose:      Launch App Manually
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Shell

# ------------------------------------------------------------------------ #

# Flask
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

export DEBUG=True
export OFFLINE=False
export PORT=8092
export OUTPUT=/Users/claramarquardt/Desktop/KnowingMe_Data
export SAFE_MODE=False

## Note: no need to set TIMEZONE_OFFSET, TIMEZONE_NAME (Run local)

## Launch app
python codebase/KnowingMe.py

# Heroku
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
heroku local web -e .env_local
heroku local web

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #


