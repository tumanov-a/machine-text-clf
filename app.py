from flask import Flask, render_template, request
from analyzer import Analyzer

app = Flask(__name__, template_folder='templates')

analyzer = Analyzer('checkpoints/bert_model_0_1.pt')

@app.route('/')
def tryit():
    return render_template('tryit.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict_label', methods=['POST'])
def predict_label():
    text = request.form['text']
    print(text)
    pred_label = analyzer.predict_label(text)
    print(pred_label)
    return render_template('tryit.html', context={'label': pred_label})

if __name__ == '__main__':
    app.run()