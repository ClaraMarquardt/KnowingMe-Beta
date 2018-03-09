# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         Manual
# Purpose:      Launch App Manually
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Shell

# ------------------------------------------------------------------------ #

# Settings

export DEBUG=True
# export DEBUG=False

# export OFFLINE=True
export OFFLINE=False

export PORT=8090

export OUTPUT=~/Desktop/KnowingMe_Data

## Launch core nlp
# java -mx4g -cp "codebase/dependencies/core_nlp/model/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -props codebase/dependencies/core_nlp/core_nlp.properties --port 9000 --timeout 10000

## Launch app
python codebase/KnowingMe.py

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #


