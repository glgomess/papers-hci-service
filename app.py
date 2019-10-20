from flask import Flask, jsonify
from flask_mysqldb import MySQL, MySQLdb

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

  cursor.execute('SELECT person_id FROM author WHERE paper_id=' + str(id))
  getAuthorName = 'SELECT person_name FROM person WHERE '
  firstTime = True
  for author in cursor:
    authorId = author['person_id']
    if firstTime:
      getAuthorName = getAuthorName + 'person_id=' + str(authorId)
      firstTime = False
    else:
      getAuthorName = getAuthorName + ' OR person_id=' + str(authorId)
  
  cursor.execute(getAuthorName)
  authors = []
  for person in cursor:
    authorName = person['person_name']
    authors.append(authorName)

  response = {
    'title': paperInfo['paper_title'],
    'abstract_PT': paperInfo['paper_abstract_PT'],
    'authors': authors
  }
  
  cursor.close()

  return jsonify(response)



if __name__ == '__main__':
  app.run(port=5000, debug=TRUE)