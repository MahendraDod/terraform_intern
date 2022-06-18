from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import boto3
import json

app = Flask(__name__)

client = boto3.client('secretsmanager')
response = client.get_secret_value(

    SecretId='prod/mydb/mydatabase'

)
secretDict = json.loads(response['SecretString'])

 
app.config['MYSQL_HOST'] = secretDict['host']

app.config['MYSQL_USER'] = secretDict['username']
  
app.config['MYSQL_PASSWORD'] = secretDict['password']
 
app.config['MYSQL_DB'] = secretDict['dbname']
 
mysql = MySQL(app)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
 
 
app.run(host='localhost', port=5000)
