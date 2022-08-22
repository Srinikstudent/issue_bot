
import os
from os import environ
import pickle
from flask import Flask, render_template, jsonify, request, Blueprint
from flask_cors import CORS
import joblib
from sklearn.model_selection import cross_val_score
import numpy as np
import cv2 as cv
from sklearn.metrics import precision_recall_fscore_support,matthews_corrcoef
from sklearn.metrics import accuracy_score, f1_score, precision_score
import csv
import pandas as pd
version = '0.0.1'
app = Flask(__name__)
CORS(app)
model = joblib.load('./notebooks/model1.sav')

flask_env = environ.get('FLASK_ENV')

    
def predict_label(issue_id, title, body, is_test):
   
    X = [title + ' ' + body]
    label = model.predict(X)
    return label[0]     
def correct_label(issue_id, correct_label):
    print('issue_id is ' + issue_id + ' corrected label is ' + correct_label)
    mylist = [] 
  # for data in (issue_id, title, body, label[0]):
    data = [issue_id, correct_label]
    mylist.append(data)
   # if len(mylist) == 1000:
   #header = ['issue_id','corredted label']
    data = mylist
    with open('corrected_label_data.csv', 'a',encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
@app.route('/form', methods=['GET'])
def form():
    """
        This is the form endpoint that you can view locally to test the system.
    """
    port = 5000
    if flask_env == 'production':
        port = 5001
    if flask_env == 'staging':
        port = 5002
    return render_template("form.html", version=version, flask_env=flask_env, correction_url=f'https://gt-srini-bot.herokuapp.com/api/correction', issue_url=f'https://gt-srini-bot.herokuapp.com/api/issue')

@app.route('/api/issue', methods=['POST'])
def predict_issue_label():
    data = request.get_json()
    label = predict_label(data['id'], data['title'], data['body'], data['test'])
    return jsonify({'id': data['id'], 'label': label})

@app.route('/api/correction', methods=['POST'])
def correct_issue_label():
    data = request.get_json()
    correct_label(data['id'], data['label'])
    return jsonify({'id': data['id']})

if __name__ == '__main__':
    app.run()
 
