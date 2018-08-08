# ----------------------------------------------------------------------------#
#----------------------------------------------------------------------- #

# KnowingMe 

# File:         aws_heroku_update
# Purpose:      Update aws/heroku image
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Shell
# Notes:

# ------------------------------------------------------------------------ #

# Heroku (Python/Flask App)
cd codebase
git add .
git commit -am "XXXX"
git push heroku master

# AWS (Docker Image (Need to first update docker image) - Run on Linux (!No Volumes))
cd codebase/aws
eb deploy

#----------------------------------------------------------------------------#


