import cv2
import numpy as np
import urllib.request

import flask

app = flask.Flask(__name__)

fase_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml');

def url_to_image(url):
    resp = urllib.request.urlopen(url);
    image = np.asarray(bytearray(resp.read()), dtype = "uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    return image

from flask import request

def _test(argument):
    return "TEST: %s" % argument

@app.route("/test", methods=["GET"])
def test():
    return "Hello its running";

@app.route("/test", methods=["POST"])
def test():
    new_quark = request.get_json()
    return new_quark['test']


@app.route('/findFaces', methods=['POST'])
def home():
    jsonImage= request.get_json()
    image_url = jsonImage['image_url']
    image = url_to_image(image_url);
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
    image = image[:,:,::-1];

    faces = fase_cascade.detectMultiScale(gray,1.3,5)

    


    try:
        faceNo = faces.shape[0];
        return("No of face detected: "+str(faceNo))
    except :
        return("No face is detected")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
