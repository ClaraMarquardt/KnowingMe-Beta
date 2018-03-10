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
# docker build -t knowingmebeta .
docker build --no-cache -t knowingmebeta .

# Push docker image
docker login --username=knowingmeatideas42        					# KnowingMe    
docker tag knowingmebeta knowingmeatideas42/knowingmebeta
docker push knowingmeatideas42/knowingmebeta

#----------------------------------------------------------------------------#


