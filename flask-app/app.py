from flask import Flask, jsonify, request, json
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL, MySQLdb
import pandas as pd
from pandas import DataFrame
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Database Configurations
app.config['MYSQL_HOST'] = '139.82.120.3'
app.config['MYSQL_USER'] = 'gabiguti'
app.config['MYSQL_PASSWORD'] = 'Pgabiguti!'
app.config['MYSQL_DB'] = 'ihc'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

@app.route('/')
def homepage():
  return "Homepage"

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
  senha = 'senha'
  username = request.json['data']['username']
  password = request.json['data']['password']
  users = {'guilherme':'senha'}

  encryptedPassword = password.encode("utf-8")
  if(encryptedPassword == senha.encode("utf-8")):
    return app.response_class(
      response=json.dumps('idunico'),
      status=200,
      mimetype='application/json'
    )
  else:
    return app.response_class(
      response=json.dumps('idunico'),
      status=403,
      mimetype='application/json'
  ) 

  # Generate hash for PW
  # Validate on DB
  # 400 if found, but wrong password
  # 403 if not found
  # 200 if OK
  # Generate unique id
  # Store ID on Redis
  # Implement HTTPS w/ SSL/TLS for secure authentication

@app.route('/papers')
def getPapers():
  cursor = mysql.connection.cursor()
  cursor.execute('SELECT paper_id, paper_year, paper_title FROM paper')
  papers = cursor.fetchall()
  cursor.close()

  papersTable = pd.DataFrame(papers)
  papersByYear = papersTable.groupby(["paper_year"])[['paper_id', 'paper_title']].apply(lambda x: x.values.tolist())
  
  return papersByYear.to_json()

@app.route('/papers/<int:id>')
def getPaperAbstractAndTitle(id):
  cursor = mysql.connection.cursor()
  cursor.execute(
    'SELECT paper_title, paper_abstract_PT '
    'FROM paper '
    'WHERE paper_id=' + str(id))
  paperInfo = cursor.fetchone()

  cursor.execute(
    'SELECT person.person_name '
    'FROM paper '
    'JOIN author ON author.paper_id = paper.paper_id '
    'JOIN person ON person.person_id = author.person_id '
    'WHERE author.paper_id=' + str(id))
  authorsTable = pd.DataFrame(cursor.fetchall())
  authors = authorsTable['person_name'].tolist() if not authorsTable.empty else []

  response = {
    'title': paperInfo['paper_title'],
    'abstract_PT': paperInfo['paper_abstract_PT'],
    'authors': authors
  }
  
  cursor.close()

  return response

@app.route('/papers/<int:id>/references')
def findPaperReferences(id):
  cursor = mysql.connection.cursor()
  cursor.execute(
    'SELECT paper_as_reference.paper_id, paper.paper_title '
    'FROM reference '
    'JOIN paper_as_reference ON paper_as_reference.reference_id = reference.reference_id '
    'JOIN paper ON paper_as_reference.paper_id = paper.paper_id '
    'WHERE reference.paper_id=' + str(id))
  referencedPapersTable = pd.DataFrame(cursor.fetchall())
  referencedPapers = referencedPapersTable.values.tolist() 

  cursor.execute(
    'SELECT reference.paper_id, paper.paper_title '
    'FROM paper_as_reference '
    'JOIN reference ON paper_as_reference.reference_id = reference.reference_id '
    'JOIN paper ON reference.paper_id = paper.paper_id '
    'WHERE paper_as_reference.paper_id=' + str(id))
  citationsTable = pd.DataFrame(cursor.fetchall())
  citations = citationsTable.values.tolist()

  response = {
    'cited': referencedPapers,
    'citedBy': citations
  }

  cursor.close()

  return response

if __name__ == '__main__':
  app.run(port=5000, debug=True)