from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
import urllib.request
import features
import model
import convertWAV
from scipy.io.wavfile import write
import config
import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np
import tensorflow
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, InputLayer, BatchNormalization, Dropout, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from matplotlib import image
import librosa
import librosa.display

from pydub import AudioSegment

rg = features.RaagAnalysis()
rp = model.raag_pred()
cwav = convertWAV.convert()

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.secret_key = config.SECRET_KEY

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
@app.route('/home')
def homescreen():
    app.logger.debug('Accessing home page')
    
    return render_template('riu.html')

@app.route('/predictions', methods=['POST', 'GET'])
def file_uploader():
    app.logger.debug('Handling file upload')
    if 'file' not in request.files:
        flash('No file found')
        return render_template('riu.html')
    
    file = request.files['file']

    if file.filename=='':
        flash('No Selection made')
        return render_template('riu.html')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.debug(f'Saving file to: {filepath}')
        file.save(filepath)
        flash('Audio uploaded successfully and the predictions are displayed')
        rg.MelSpec_Pitch(filepath)
        raaga = rp.pred(filepath)
        return render_template('results.html', raaga = raaga)
    
    else:
        flash('Allowed input formats: wav, mp3, m4a')
        return render_template('riu.html')

@app.route('/exportrec', methods=['POST', 'GET'])
def export_rec():
    app.logger.debug('Handling recording export')
    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        flash('No file found')
        return render_template('riu.html')
    
    file = request.files['file']
    if file.filename == '':
        app.logger.error('No file selected')
        flash('No file selected')
        return render_template('riu.html')
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    app.logger.debug(f'Saving recording to: {filepath}')
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            app.logger.debug(f'Removed existing file: {filepath}')
        
        file.save(filepath)
        app.logger.debug(f'Successfully saved file: {filepath}')
        
        cwav.to_wav(filepath)
        app.logger.debug('File conversion completed')
        
        flash('Recording uploaded successfully. Press predict to get results')
        return render_template('riu.html')
    except Exception as e:
        app.logger.error(f'Error processing file: {str(e)}')
        flash('Error processing recording')
        return render_template('riu.html')

@app.route('/predictRec', methods=['POST', 'GET'])
def predict_recording():
    app.logger.debug('Predicting recording')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'new_sample.wav')
    rg.MelSpec_Pitch(filepath)
    raaga = rp.pred(filepath)
    return render_template('results.html', raaga = raaga)

if __name__=='__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.logger.debug(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    app.run(debug=True, host='0.0.0.0', port=8000)
