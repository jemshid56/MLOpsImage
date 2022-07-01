import os
from PIL import Image
import io
from flask import Flask,Blueprint,request,render_template,jsonify,Response,send_file, flash
import jsonpickle
import numpy as np
import json
import base64
import generate_caption as gc

app = Flask(__name__)
static_dir='images/'
filename = "test.jpg"

app.config['UPLOAD_FOLDER'] = static_dir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            captions=gc.generate_captions(static_dir+filename)
            cap={"captions":captions}
            with open("text/data.json","w") as fjson:
                        json.dump(cap,fjson)
            #flash(cap)
            return render_template("index.html", prediction = cap, img_path = static_dir+filename)

@app.route('/result')
def sendImage():
    return send_file(static_dir+filename,mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9874)