from scipy.stats import zscore
import numpy as np
import random 
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('osi_model.sav', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

def process():

    input_features = []
    req = request.form
    city = req.get("city").upper()
    city = city[:4]
    input_features.append(random.randint(0,21))

    name = req.get("name").upper()
    name = name[:4]
    input_features.append(random.randint(0,369))

    seats = req.get("seats")
    input_features.append(seats)
    
    screens =  req.get("screens")
    input_features.append(screens)

    if req.get("type").upper() == 'MULTIPLEX':
        input_features.append(1)
    else:
        input_features.append(0)
    
    input_features = list(map(int, input_features))
    input_features = zscore(input_features)
    
    return input_features

@app.route('/predict',methods=['POST'])

def predict():

    int_features = process()
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Price of ticket should be  {}'.format(output))

@app.route('/results',methods=['POST'])

def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
