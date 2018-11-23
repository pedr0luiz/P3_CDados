from flask import Flask,session,request,render_template,redirect,url_for
from random import *
import smtplib
import base64
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from PIL import Image
import io
from resizeimage import resizeimage
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import json
import cv2
import random

# Reading Excel with ML training data
airplane = pd.read_csv('static/Excels_Classfier/Airplane3K.csv')
octopus = pd.read_csv('static/Excels_Classfier/Octopus3K.csv')
pants = pd.read_csv('static/Excels_Classfier/Pants3K.csv')
cup = pd.read_csv('static/Excels_Classfier/Cup3K.csv')
flower = pd.read_csv('static/Excels_Classfier/Flower3K.csv')
airplane['array'] = airplane['array'].apply(json.loads)
flower['array'] = flower['array'].apply(json.loads)
octopus['array'] = octopus['array'].apply(json.loads)
cup['array'] = cup['array'].apply(json.loads)
pants['array'] = pants['array'].apply(json.loads)


treinamento = pd.concat([pants,octopus,cup,flower]).sample(frac=1)
DataTreino = list(treinamento['array'])
ClassTreino = list(treinamento['word'])
Modelo = RandomForestClassifier()
Modelo.fit(DataTreino,ClassTreino)
Categorias = ['Avião',"Flor","Polvo","Copo","Calça"]


app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/draw',methods=['GET','POST'])
def Draw():
    if request.method == 'POST':
        DOMString = request.form['DOMString']
        DOMString_Lista = DOMString.split(',')
        ImgDecoded = base64.b64decode(DOMString_Lista[1])
        img = Image.open(io.BytesIO(ImgDecoded))
        ImageReal = resizeimage.resize_cover(img,[108,72])
        #ImageReal.show()
        ImageReal.save('Teste.png')
        ImageArray = np.array(ImageReal)
        Array = (cv2.cvtColor(ImageArray, cv2.COLOR_RGB2GRAY).flatten()/255)
        ArrayFinal = list(Array)
        ArrayFinal2 = [ArrayFinal]
        predicao = Modelo.predict(ArrayFinal2)
        return render_template('resultado.html',resultado=predicao)
    else:
        categoriaSelecionada = random.choice(Categorias)
        return render_template('drawing.html',categoria=categoriaSelecionada )
if __name__ == '__main__':
    app.run(debug=True)
