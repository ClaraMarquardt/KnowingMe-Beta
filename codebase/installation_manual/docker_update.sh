# ----------------------------------------------------------------------------#
#----------------------------------------------------------------------- #

# KnowingMe 

# File:         docker_update
# Purpose:      Update docker image
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Shell
# Notes:

# ------------------------------------------------------------------------ #

# Build docker image
# docker build -t knowingmeaws .
# docker build --no-cache -t knowingmeaws .
docker build --build-arg RESTART=`date +%s` -t knowingmeaws .

# Push docker image
docker login --username=knowingmeapp        		# KnowingMe    
docker tag knowingmeaws knowingmeapp/knowingmeaws
docker push knowingmeapp/knowingmeaws

#----------------------------------------------------------------------------#


