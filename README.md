# Service for IHC papers database 

Back-end service to access IHC Database on MySQL and provide endpoints to perform queries on the database.

## Getting Started on Docker

### Prerequisites
- Have [Docker](https://docs.docker.com/get-docker/) installed on your machine

### Installing
1. Clone this repository
2. Download [mysql-connector-java:5.1.46](https://jar-download.com/artifacts/mysql/mysql-connector-java/5.1.46/source-code)
3. Save the folder as `mysql-connector-java-5.1.46` inside `docker-container/docker-logstash-image/`
4. On terminal go to `docker-container` folder
5. Run `docker build -t logstash-image:1.0 docker-logstash-image/`
6. Run `docker-compose up --build`

Your containers should be up and running!
Check ElasticSearch with: `curl -X GET "localhost:9200/_cat/nodes?v&pretty"`
Check Kibana on: `http://localhost:5601`
Check indexed data with: ``curl -X GET "localhost:9200/papers/_search"`

## Docker container - v2

Composed containers used to pull data from IHC Database on MySQL an index it on ElastiSearch, to be able to perform more complex operations like text search and analysis. \
See `/docker-container/README.md` to further information.

## Flask application - v1

Service to retrieve data from IHC database using Flask application. And provide localhost endpoints to fetch resources. \
See `/flask-app/README.md` to further information.

## Built with
- [Docker](https://www.docker.com/) - Composed containers to integrate MySQL and ElasticSearch
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Back-end service from MySQL to localhost endpoints

## Authors
- Gabriela Gutierrez - @gabibguti