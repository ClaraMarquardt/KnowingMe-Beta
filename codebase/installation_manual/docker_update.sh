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
# docker build -t knowingmebeta_test .
# docker build --no-cache -t knowingmebeta_test .
docker build --build-arg RESTART=`date +%s` -t knowingmebeta_test .

# Push docker image
docker login --username=knowingmeatideas42        					# KnowingMe    
docker tag knowingmebeta_test knowingmeatideas42/knowingmebeta_test
docker push knowingmeatideas42/knowingmebeta_test

#----------------------------------------------------------------------------#


