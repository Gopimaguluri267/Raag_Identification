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
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, InputLayer, BatchNormalization, Dropout, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint
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
app.secret_key = 'gop!'

allowed_extensions = set(['wav', 'mp3', 'm4a'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions


@app.route('/')
def homescreen():
    return render_template('riu.html')

@app.route('/predictions', methods=['POST', 'GET'])
def file_uploader():
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
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    cwav.to_wav(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if 'file' in request.files:
        flash('Recording uploaded successfully. Press predict to get results')
    return render_template('riu.html')

@app.route('/predictRec', methods=['POST', 'GET'])
def predict_recording():
    rg.MelSpec_Pitch('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    raaga = rp.pred('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav')
    except:
        pass
    try:
        os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/tempPlot.jpg')
    except:
        pass
    return render_template('results.html', raaga = raaga)


#     try:
#         print('Finallyy aage ethee.')
#         print(request.form)
#         print(request.files)
#         if ('file' in request.form):
#             file = request.files['file']
#             filename = secure_filename(file.filename)
#             directory = os.path.join(os.getcwd(), 'temp-data')
#             # logging.info("[INFO] Object Recognition: Image file passed validations...")
#             if not os.path.exists(directory):
#                 os.makedirs(directory)
#             file_save_path = os.path.join(directory, filename)
#             file.save(file_save_path)
#             print('file saved locally')
#             file_save_path = 'C:/Users/Gopi Maguluri/Raag Identification and Understanding/FRIU/static/uploads'
#             with open(file_save_path, "rb") as file:
#                 b_str = base64.b64encode(file.read())
#             return render_template('riu.html')
#     except Exception as e:
#         print('exception logged', e)



if __name__=='__main__':
    app.run(debug=True,port=8500)
