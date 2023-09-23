from flask import Flask,render_template,redirect,request
import os
from PIL import Image
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pathlib import Path
import numpy as np
from werkzeug.utils import secure_filename
app=Flask(__name__)

def predict(img_path):
    path=Path('artifacts/distractdriver2.h5')
    model=load_model(path)
    img=image.load_img(img_path,target_size=(224,224))
    img=image.img_to_array(img)
    img=img/255
    img = np.expand_dims(img, axis=0)
    result_response=model.predict(img)
    return np.argmax(result_response[0],axis=0)  

@app.route('/')
def home():
   return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def result():
   driver_action={
    'c0': 'normal driving',
    'c1': 'texting - right',
    'c2': 'talking on the phone - right',
    'c3': 'texting - left',
    'c4': 'talking on the phone - left',
    'c5': 'operating the radio',
    'c6': 'drinking',
    'c7': 'reaching behind',
    'c8': 'hair and makeup',
    'c9': 'talking to passenger'
   }
   if request.method == 'POST':
      image=request.files['driver_img']
      path=os.path.join('static',secure_filename(image.filename))
      image.save(path)
      result_response=predict(path)
      result=driver_action['c'+str(result_response)]
      image_path=Path('static/'+image.filename)
      print(image_path)
      return render_template("predict.html",result=result,image_path=image_path)
if __name__ == '__main__':
   app.run(debug = True ,host="0.0.0.0", port=8080)