from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
import urllib.request
import features
import model
import convertWAV
from scipy.io.wavfile import write

# model 
import numpy as np
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, InputLayer, BatchNormalization, Dropout, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.utils import generic_utils
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image
import librosa
import librosa.display

#features
import numpy as np 
import matplotlib.pyplot as plt
from pydub import AudioSegment
import librosa
import librosa.display
import parselmouth


rg = features.RaagAnalysis()
rp = model.raag_pred()
cwav = convertWAV.convert()

upload_folder = "/home/ubuntu/raag-identification/Raag_Identification/static/uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/ubuntu/raag-identification/Raag_Identification/static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 20*1024*1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'gop!'

allowed_extensions = set(['wav', 'mp3', 'm4a'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions


@app.route('/')
def homescreen():
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/tempPlot.png')
    except:
        pass
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    except:
        pass
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/sample.wav')
    except:
        pass
    return render_template('riu.html')

@app.route('/predictions', methods=['POST', 'GET'])
def file_uploader():
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/tempPlot.png')
    except:
        pass
    
    if 'file' not in request.files:
        flash('No file found')
        return render_template('riu.html')
    
    file = request.files['file']

    if file.filename=='':
        flash('No Selection made')
        return render_template('riu.html')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Audio uploaded successfully and the predictions are displayed')
        rg.MelSpec_Pitch(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        raaga = rp.pred(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # plots=[]
        # for i in os.listdir(up_f):
        #     if ((i[:-3])=='tempPlot') and ((i[-3:])=='jpg'):
        #         plots.append(i)
        return render_template('results.html', raaga = raaga)
    
    else:
        flash('Allowed input formats: wav, mp3, m4a')
        return render_template('riu.html')


@app.route('/exportrec', methods=['POST', 'GET'])
def export_rec():
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/tempPlot.png')
    except:
        pass
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     cwav.to_wav(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if 'file' in request.files:
        flash('Recording uploaded successfully. Press predict to get results')
    print("Uploading Done...press Predict")
    return render_template('riu.html')

@app.route('/predictRec', methods=['POST', 'GET'])
def predict_recording():
    cwav.to_wav('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/sample.wav')
    rg.MelSpec_Pitch('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    raaga = rp.pred('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    except:
        pass
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/sample.wav')
    except:
        pass
    return render_template('results.html', raaga = raaga, cache=False)


if __name__=='__main__':
    app.run(debug=True,port=8500)
