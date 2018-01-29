# Common docker commands
# ---------------------------------

## KnowingMe Image
## ---------------------

# Build docker image
docker build -t knowingme .
docker build --no-cache -t knowingme .

# Push docker image
docker login --username=claramarquardt          # knowingme
docker tag knowingme claramarquardt/knowingme
docker push claramarquardt/knowingme

# Pull & Run Image
docker pull claramarquardt/knowingme
docker run -p 8000:8000 claramarquardt/knowingme

## Generic Docker Commands
## ---------------------

# List all containers
docker ps -a

# Delete image
docker rmi claramarquardt/knowingme

# Stop all images
docker stop $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

## Push to Heroku App
## ---------------------
# heroku login
# heroku container:login
# docker tag knowingme registry.heroku.com/knowingme/web
# docker push registry.heroku.com/knowingme/web
# https://knowingme.herokuapp.com/