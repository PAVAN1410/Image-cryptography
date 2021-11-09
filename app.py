from flask import Flask, render_template, url_for, request, send_file, redirect
from werkzeug.utils import secure_filename
import sys
import os
import glob
import re
import numpy as np
from encrypt import *
from decrypt import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt():
    if request.method == 'POST':
        f = request.files['image']
        f.save(secure_filename('test.png'))

        result=request.form
        encrypt_image('test.png')
        p = "webzip.zip"
        return send_file(p,as_attachment=True)
        # return render_template('encryption.html')
    elif request.method=='GET': 
        result=request.form
        return render_template('encryption.html')

@app.route('/decrypt', methods=['POST', 'GET'])
def decrypt():
    if request.method == 'POST':
        f = request.files['image']
        f.save(secure_filename('test.zip'))

        result=request.form
        decrypt_image('test.zip')
        p = "decrypted_images/decrypted_image.png"
        return send_file(p,as_attachment=True)
        # return render_template('decryption.html')
    elif request.method=='GET': 
        result=request.form
        return render_template('decryption.html')



@app.route('/help')
def help():
    return render_template('help.html')

if __name__ =='__main__':
    app.run(debug=True)

