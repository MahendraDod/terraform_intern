from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import boto3
import base64
import json

app = Flask(__name__)

session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name= "ap-south-1"
)

get_secret_value_response = client.get_secret_value(
    SecretId = "prod/mydb/database"
)
if 'SecretString' in get_secret_value_response:
    secret = get_secret_value_response['SecretString']
else:
    secret = decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
secretdict = json.loads(secret)

 
app.config['MYSQL_HOST'] = secretdict['host']

app.config['MYSQL_USER'] = secretdict['username']
  
app.config['MYSQL_PASSWORD'] = secretdict['password']
 
app.config['MYSQL_DB'] = secretdict['dbname']
 
mysql = MySQL(app)
 
def load_keras_model():
    """Load in the pre-trained model"""
    global model
    model = load_model('../models/train-embeddings-rnn.h5')
    # Required for model to work
    global graph
    graph = tf.get_default_graph() 

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
        
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_keras_model()
    # Run app
    app.run(host="0.0.0.0", port=80) 
