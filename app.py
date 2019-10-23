from flask import Flask, jsonify
from flask_mysqldb import MySQL, MySQLdb
import pandas as pd
from pandas import DataFrame

app = Flask(__name__)

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

@app.route('/papers')
def getPapers():
  cursor = mysql.connection.cursor()
  cursor.execute('SELECT paper_id, paper_year, paper_title FROM paper')
  data = cursor.fetchall()
  cursor.close()

  return jsonify(data)

@app.route('/papers/<int:id>')
def getPaperAbstractAndTitle(id):
  cursor = mysql.connection.cursor()
  cursor.execute('SELECT paper_title, paper_abstract_PT FROM paper WHERE paper_id=' + str(id))
  paperInfo = cursor.fetchone()

  getAuthors = 'SELECT person.person_name FROM paper JOIN author ON author.paper_id = paper.paper_id JOIN person ON person.person_id = author.person_id WHERE author.paper_id=' + str(id)
  cursor.execute(getAuthors)

  authorsTable = pd.DataFrame(cursor.fetchall())
  authors = authorsTable['person_name'].tolist()

  response = {
    'title': paperInfo['paper_title'],
    'abstract_PT': paperInfo['paper_abstract_PT'],
    'authors': authors
  }
  
  cursor.close()

  return response

if __name__ == '__main__':
  app.run(port=5000, debug=TRUE)