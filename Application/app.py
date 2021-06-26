from flask import Flask, render_template, request,jsonify
from keras.models import load_model
import cv2 , base64 ,io ,re
import numpy as np
from PIL import Image
from flask_cors import CORS
img_size=100
app = Flask(__name__) 
CORS(app)
model007=load_model('model-007.model')
dictionnaire={0:'Test Covid19 Négatif', 1:'Test Covid19 Positif'}
def preprocess(img):
	img=np.array(img)
	if(img.ndim==3):
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	else:
		gray=img
	gray=gray/255
	resized=cv2.resize(gray,(img_size,img_size))
	reshaped=resized.reshape(1,img_size,img_size)
	return reshaped
@app.route("/")
def index():
	return(render_template("index.html"))
@app.route("/predict", methods=["POST"])
def predict():
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	dataBytesIO=io.BytesIO(decoded)
	dataBytesIO.seek(0)
	image = Image.open(dataBytesIO)
	test_image=preprocess(image)
	prediction = model007.predict(test_image)
	resultat=np.argmax(prediction,axis=1)[0]
	precision=float(np.max(prediction,axis=1)[0])
	label=dictionnaire[resultat]
	response = jsonify({'prediction': {'resultat': label,'precision': precision}})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
app.run(debug=True)