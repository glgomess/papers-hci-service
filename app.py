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

@app.route('/test')
def getPapers():
  cursor = mysql.connection.cursor()
  cursor.execute('SELECT * FROM author;')
  data = cursor.fetchall()
  cursor.close()

  return jsonify(data)

if __name__ == '__main__':
  app.run(port=5000, debug=TRUE)