import os
import requests

from flask import Flask, render_template, request, jsonify
from analyzer import Analyzer

from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

analyzer = Analyzer('checkpoints/bert_model_0_1.pt')


app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
 
def create_database():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''USE flask''')
        cur.execute('''CREATE TABLE nlg_label (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        text TEXT,
                        label INT
                        )''')
        mysql.connection.commit()

mysql = MySQL(app)

tasks = [
    {
        'id': 1,
        'title': u'Predict label',
        'description': u'Predict label for machine or human text', 
    },
    {
        'id': 2,
        'title': u'Insert label in database',
        'description': u'Insert correct label of text in database', 
    },
    {
        'id': 3,
        'title': u'Get database',
        'description': u'Get full database data', 
    }
]

@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1.0/get_data', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM nlg_label''')
    rv = cur.fetchall()
    return jsonify({'database': rv})

@app.route('/api/v1.0/predict_label', methods=['POST'])
def predict_label(data):
    text = data['text']
    pred_label, pred_prob = analyzer.predict_label(text)
    return jsonify({'label': pred_label, 'prob': pred_prob, 'text': text})

@app.route('/api/v1.0/insert_label', methods=['POST'])
def insert_label(data):
    text = data['text']
    label = data['label']
    correct = data['correct']
    label = 0 if label == 'Human' else 1
    if correct == 'incorrect':
        labels = [0, 1]
        labels.pop(label)
        label = labels[0]
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO nlg_label (text, label) VALUES(%s, %s)''', (text, label))  
    mysql.connection.commit()
    return jsonify({'text': text, 'label': label})

@app.route('/')
def tryit():
    return render_template('tryit.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/db')
def db():
    response = get_data()
    return render_template('db.html', db=response.get_json()['database'])

@app.route('/label', methods=['POST'])
def label():
    text = request.form['text']
    response = predict_label({'text': text})
    return render_template('tryit.html', context=response.get_json())

@app.route('/new_text', methods=['POST'])
def new_text():
    text = request.form['text']
    label = request.form['label']
    correct = request.form['insert_label_button']
    response = insert_label({'text': text, 'label': label, 'correct': correct})
    return render_template('tryit.html', new_text_response=response.get_json())

if __name__ == '__main__':
    create_database()
    app.run(debug=True)