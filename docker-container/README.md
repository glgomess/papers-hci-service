# Running docker

## Useful commands

List all docker containers: `docker ps -a` \
Start container: `docker start CONTAINER_ID` \
Kill container: `docker container kill CONTAINER_ID` \
Delete container: `docker container rm CONTAINER_ID` \
Run terminal inside container: `docker exec -it CONTAINER_ID bash`

## Logstash Container

**Attempt #1** \
Create logstash container but cannot change config files: \
`docker run --name="logstash-container" -p 5044:5044 docker.elastic.co/logstash/logstash:7.7.0`

**Attempt #2** \
Create a Dockerfile to configure the logstash container I would like to create, i.e. create an image for this container. \
Building the docker image: \
`docker build -t {TAG_NAME}:{TAG_VERSION} {PATH_DOCKERFILE}` \
`docker build -t logstash-image:1.0 docker-logstash-image/`
```bash
Sending build context to Docker daemon  11.32MB
Step 1/3 : FROM docker.elastic.co/logstash/logstash:7.7.0
 ---> 30dcca1db5e9
Step 2/3 : RUN rm -f /usr/share/logstash/pipeline/logstash.conf
 ---> Running in b2390727de20
Removing intermediate container b2390727de20
 ---> 7ab3ee62c572
Step 3/3 : ADD config/ /usr/share/logstash/config/
 ---> c07720cca8b6
Successfully built c07720cca8b6
Successfully tagged logstash-image:1.0
```

## Docker composed containers

Create a docker-compose.yml file. \
Running the composed container: \
`docker-compose up --build`