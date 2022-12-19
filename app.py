from flask import Flask, render_template
from analyzer import Analyzer

app = Flask(__name__)

analyzer = Analyzer('checkpoints/bert_model_0_1.pt')

@app.route('/')
def tryit():
    return render_template('tryit.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict_label', methods=['POST'])
def predict_label(text):
    pred_label = predict_label(text)
    return render_template('tryit.html', context=pred_label)

if __name__ == '__main__':
    app.run()