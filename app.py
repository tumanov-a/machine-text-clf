from flask import Flask, render_template, request, jsonify
from analyzer import Analyzer

from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

analyzer = Analyzer('checkpoints/bert_model_0_1.pt')

app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234567890'
app.config['MYSQL_DB'] = 'flask'
#app.config['MYSQL_PORT'] = 5060
 
mysql = MySQL(app)

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
    cur = mysql.connection.cursor()
    s = cur.execute('''SELECT * FROM nlg_label''')
    rv = cur.fetchall()
    mysql.connection.commit()
    return render_template('db.html', db=rv)

@app.route('/predict_label', methods=['POST'])
def predict_label():
    text = request.form['text']
    pred_label, pred_prob = analyzer.predict_label(text)
    return render_template('tryit.html', context={'label': pred_label, 'prob': pred_prob, 'text': text})

@app.route('/insert_label', methods=['POST'])
def insert_label():
    text = request.form['text']
    print("request.form text: {}".format(text))
    label = request.form['label']
    print("request.form label: {}".format(label))
    correct = request.form['insert_label_button']
    print("correctness: {}".format(correct))
    label = 0 if label == 'Human' else 1
    if correct == 'incorrect':
        labels = [0, 1]
        labels.pop(label)
        label = labels[0]
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO nlg_label (text, label) VALUES(%s, %s)''', (text, label))  
    mysql.connection.commit()
    return render_template('tryit.html')

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/get_data', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    s = cur.execute('''SELECT * FROM nlg_label''')
    rv = cur.fetchall()
    return jsonify({'get_data': rv})

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
