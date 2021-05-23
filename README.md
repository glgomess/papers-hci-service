# Service for IHC papers database 

Back-end service to access IHC Database on MySQL and provide endpoints to perform queries on the database.

## Getting Started on Docker

### Prerequisites
- Have [Docker](https://docs.docker.com/get-docker/) installed on your machine

### Installing (easy configuration)
1. Clone this repository
2. Download [mysql-connector-java:5.1.46](https://jar-download.com/artifacts/mysql/mysql-connector-java/5.1.46/source-code)
3. Save the folder as `mysql-connector-java-5.1.46` inside `docker-container/docker-logstash-image/`
4. On terminal go to `docker-container` folder
5. Check if `docker-compose.yml` file has the correct MYSQL database information (MYSQL_HOST, MYSQL_PORT, DATABASE_NAME, MYSQL_USER, MYSQL_USER_PASSWORD)
6. Run `docker build -t logstash-image:1.20 docker-logstash-image/`
7. Run `docker-compose up --build`

Your containers should be up and running! \
Check ElasticSearch with: `curl -X GET "localhost:9200/_cat/nodes?v&pretty"` \
Check Kibana on: `http://localhost:5601` \
Check indexed data with: `curl -X GET "localhost:9200/papers/_search"` \
Check **DEFAULT** `papers` index mapping: `curl -XGET "http://es01:9200/papers/_mapping"`

### Installing (complete configuration)
1. Clone this repository
2. Download [mysql-connector-java:5.1.46](https://jar-download.com/artifacts/mysql/mysql-connector-java/5.1.46/source-code)
3. Save the folder as `mysql-connector-java-5.1.46` inside `docker-container/docker-logstash-image/`
4. On terminal go to `docker-container` folder
5. Check if `docker-compose.yml` file has the correct MYSQL database information (MYSQL_HOST, MYSQL_PORT, DATABASE_NAME, MYSQL_USER, MYSQL_USER_PASSWORD)
6. Comment logstash configuration in `docker-compose.yml`:
```
  # logstash:
  #     image: logstash-image:1.16
  #     container_name: logstash
  ...
  #     depends_on:
  #       - es01
  #       - kibana
```
7. Run `docker-compose up --build`
8. Check if your cluster is up and running with:
```
curl -XGET "http://localhost:9200/_cluster/health"
```
9. Then, create new index `papers` by running:
```
curl -XPUT "http://localhost:9200/papers" -H 'Content-Type: application/json' -d'{  "mappings" : {    "properties" : {      "paper_abstract_en" : {        "type" : "text",        "analyzer": "english"      },      "paper_abstract_es" : {        "type" : "text",        "analyzer": "spanish"      },      "paper_abstract_pt" : {        "type" : "text",        "analyzer": "brazilian"      },      "paper_acm_category" : {        "type" : "text"      },      "paper_acm_key" : {        "type" : "text"      },      "paper_acm_terms" : {        "type" : "text"      },      "paper_authors" : {        "type" : "text"      },      "paper_id" : {        "type" : "keyword"      },      "paper_language" : {        "type" : "keyword"      },      "paper_num_authors" : {        "type" : "long"      },      "paper_references" : {        "properties": {          "paper_reference": {            "type": "text"          },          "paper_reference_id": {            "type": "integer"          }        }      },      "paper_theme" : {        "type" : "text",        "fields" : {          "keyword" : {            "type" : "keyword",            "ignore_above" : 256          }        }      },      "paper_title" : {        "type" : "text"              },      "paper_year" : {        "type" : "integer"      }    , "paper_keywords": {        "type" : "text"      }
}  }}'
```

9.1 create a new index `authors` by running:

```
curl -XPUT "http://localhost:9200/authors" -H 'Content-Type: application/json' -d'{  "mappings" : {    "properties" : { "person_name" : { "type" : "text" },
  "person_name_in_ref" : { "type" : "text" }, "papers_list": { "type" : "text" }, "person_id": { "type" : "text" }
}}} '      
```

9.2 create a new index `keywords` by running:

```
curl -XPUT "http://localhost:9200/keywords" -H 'Content-Type: application/json' -d'{  "mappings" : {    "properties" : { "keyword_id" : { "type" : "text" }, "keyword_EN" : { "type" : "text" }, "papers_list": { "type" : "text" }
}}} '      
```

10. Uncomment logstash configuration in `docker-compose.yml`
11. Run `docker build -t logstash-image:1.25 docker-logstash-image/`
12. Run `docker-compose up --build`

Your containers should be up and running! \
Check ElasticSearch with: `curl -X GET "localhost:9200/_cat/nodes?v&pretty"` \
Check Kibana on: `http://localhost:5601` \
Check indexed data with: `curl -X GET "localhost:9200/papers/_search"` \
Check **CUSTOM** `papers` index mapping: `curl -XGET "http://es01:9200/papers/_mapping"`

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