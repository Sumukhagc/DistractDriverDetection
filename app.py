from flask import Flask,render_template,redirect,request
import os
from PIL import Image
import random
app=Flask(__name__)

@app.route('/')
def home():
   return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def result():
   if request.method == 'POST':
      image=request.files['driver_img']
      print(request.form)
      print(type(image))
      img = Image.open(image)
      img.convert("RGB")
      image_name='img'+str(random.randint(0,1000000))+'.jpg'
      path=os.path.join('images',image_name)
      img.save(path) 
      
      return render_template("predict.html",sentiment='sentiment')
if __name__ == '__main__':
   app.run(debug = True ,host="0.0.0.0", port=8080)