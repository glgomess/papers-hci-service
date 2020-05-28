# Docker for IHC Database

## Docker compose

### About the docker tool
Docker compose is a useful tool to declare multiple containers at a glance and specify relations between them. This way we can guarantee that Logstash service starts after ElasticSearch service. And that both containers will start together, because they are directly related and it wouldn't make sense to run only Logstash, for example. \
Read more about docker compose here: https://docs.docker.com/compose/

### Using docker compose for IHC database
Here, we are using docker compose to start together 3 services: ElasticSearch, Kibana and Logstash. \
ElasticSearch is where we are going to save our data, but in another form. \
Kibana is an analysis application for ElasticSearch. \
And Logstash is a pipeline that allows processing and injecting data from place A into place B. In our case from MySQL Database into ElasticSearch.

**Main Objective: Put the database information in ElasticSearch to perform search and data analysis easily, specially on texts.**

### Creating the docker-compose.yml file

Our docker-compose is divided in 4 sections: version, services, volumes and networks. \
version: defines the version of docker compose we are using to build this file. \
services: declare our services: ElasticSearch, Kibana and Logstash. \
volumes: declare paths to save our data. Useful for when container restarts to be used as backup data. \
networks: just to explict that all of our services are running in the same network here. \

#### ElasticSearch
```yml
  elasticsearch:
      # Cloning elasticsearch official docker image (version 7.7.0)
      image: docker.elastic.co/elasticsearch/elasticsearch:7.7.0
      # Naming the container
      container_name: elasticsearch
      # Run on port 9200 inside docker container
      ports:
        - 9200:9200
      # Define a single node instance and the cluster name
      environment:
        - node.name=elasticsearch
        - cluster.name=es-docker-cluster
        - bootstrap.memory_lock=true
        - discovery.type=single-node
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      # Separate a folder to elasticsearch to keep a backup of our data (used on container restart)
      volumes:
        - data01:/usr/share/elasticsearch/data
      networks:
        - elastic
```
#### Kibana
```yml
  kibana:
      # Just cloning kibana official docker image as well (version 7.7.0)
      image: docker.elastic.co/kibana/kibana:7.7.0
      container_name: kibana
      ports:
        - 5601:5601
      networks:
        - elastic
      # This tells kibana to start only after elasticsearch
      depends_on:
        - elasticsearch
```
#### Logstash
```yml
  logstash:
      # THIS IS SPECIAL: Here we are cloning a custom docker image called "logstash-image" on version 1.6
      image: logstash-image:1.6
      container_name: logstash
      ports:
          - 5044:5044
      # Here we define our custom environment variables that are used inside our custom logstash pipeline
      environment:
          - LOGSTASH_JDBC_DRIVER_JAR_LOCATION=/lib/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46-bin.jar
          - LOGSTASH_JDBC_DRIVER=com.mysql.jdbc.Driver
          - MYSQL_HOST=host.docker.internal
          - MYSQL_PORT=3306
          - DATABASE_NAME=ihc
          - MYSQL_USER=root
          - MYSQL_USER_PASSWORD=bonjovi7
          - ELASTIC_INDEX=papers
          - ELASTIC_DOC_TYPE=paper
      networks:
        - elastic
      # This tells logstash to start only after elasticsearch and kibana
      depends_on:
        - elasticsearch
        - kibana
```

### Running the composition
`docker-compose up --build`

## Custom Logstash

Here we do a logstash clone from official logstash docker image. BUT including custom configurations on the pipeline. \
In the configuration file we tell logstash to pull data from MySQL Database and index it into ElasticSearch.

### Attempt #1 - Logstash container - FAIL
Created logstash container but cannot change config files. \
`docker run --name="logstash-container" -p 5044:5044 docker.elastic.co/logstash/logstash:7.7.0`

### Attempt #2 - Logstash image - SUCCESS

In the Dockerfile we are able to copy a local file `logstash.conf` to inside the container. And instruct the container to run these configurations. \
And in the `logstash.conf` file we define the pipeline from MySQL to ElasticSearch. \
`docker build -t {TAG_NAME}:{TAG_VERSION} {PATH_DOCKERFILE}` \
`docker build -t logstash-image:1.0 docker-logstash-image/` \

**AND THAT'S HOW IT ROLLS** \
When we run the docker compose, logstash container is configured to build this image. And this image when is ran starts the configurated pipeline, and starts pulling data from MySQL and outputing into a ElasticSearch index.

## Useful commands

List all docker containers: `docker ps -a` \
Start container: `docker start CONTAINER_ID` \
Kill container: `docker container kill CONTAINER_ID` \
Delete container: `docker container rm CONTAINER_ID` \
Run terminal inside container: `docker exec -it CONTAINER_ID bash`

## Authors
- Gabriela Gutierrez - @gabibguti