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
  cursor.execute('SELECT paper_id, paper_year, paper_title FROM paper;')
  data = cursor.fetchall()
  cursor.close()

  return jsonify(data)

@app.route('/papers/<int:id>')
def getPaperAbstractAndTitle(id):
  cursor = mysql.connection.cursor()
  cursor.execute('SELECT paper_title, paper_abstract_PT FROM paper WHERE paper_id=' + str(id) + ';')
  data = cursor.fetchall()
  cursor.close()

  return jsonify(data)

if __name__ == '__main__':
  app.run(port=5000, debug=TRUE)