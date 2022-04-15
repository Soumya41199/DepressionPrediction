import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import time
import joblib

app = Flask(__name__)
model = joblib.load('RF.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/',methods = ['GET', 'POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [(x) for x in request.form.values()]
    features = [] 
    for i in range(0,7):
        features.append(int_features[i])
    
    final_features = [np.array(features)]
    print(final_features)
    prediction = model.predict(final_features)
    print(prediction)
    output = prediction[0]
    if output == 1:
        return render_template('index.html', prediction_text="You are most likely in Depression. Take the Psychometric Evaluation Now and Get Help -")

    else:
        return render_template('index.html', prediction_text='You are NOT in Depression!')
    print(output)


@app.route('/evaluate')
def newtemp():
    return render_template('quest.html')

@app.route('/evaluate',methods = ['GET', 'POST'])
def evaluate():
    if request.method=='POST':
        res = [x for x in request.form.values()] 
        print(res)
        sum = 0
        for i in res:
            if i=='o1':
                sum=sum+0
            elif i=='o2':
                sum=sum+2
            elif i =='o3':
                sum=sum+4
            elif i =='o4':
                sum=sum+6
        
        print(sum)
        perc = (sum/60)*100
        perc = round(perc, 2)
        print(perc)
        val = str(perc)
        
        if(perc<=10):
            return render_template('result.html', depscore="You're not in Depression. If someone around you is struggling,refer them to this page")
        elif(perc>10 and perc<=25):
            return render_template('result.html', depscore="You're in the Early Stage of Depression with a depression score of "+val+". Refer to this page for more details and seek help right away")
        elif(perc>25 and perc<=50):
            return render_template('result.html', depscore="You've Mild Depresion with a depression score of "+val+". Refer to this page for more details and seek help right away")
        elif(perc>50 and perc<=75):
            return render_template('result.html', depscore="You've Moderate Depresion with a depression score of "+val+". Refer to this page for more details and seek help right away")
        else:
            return render_template('result.html', depscore="You've Severe Depresion with a depression score of "+val+". Refer to this page for more details and seek help right away")
            

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)