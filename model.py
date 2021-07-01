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

class raag_pred():
    def pred(self, x):
        samples, sampling_rate = librosa.load(x)
        stft = np.abs(librosa.stft(samples))**2
        M = librosa.feature.melspectrogram(S=stft)
        M = librosa.feature.melspectrogram(y=samples, sr=sampling_rate, n_mels=128, fmax=8000)
        log_M = librosa.power_to_db(M, ref=np.max)
        plt.figure(figsize=(5.04,4.32))
        plt.subplot('211')
        librosa.display.specshow(log_M, y_axis='mel', fmax=8000, x_axis='time')
        plt.tight_layout()
#         t='.jpg'
#         name=x[:-4]+t
        plt.savefig('/home/ubuntu/raag-identification/Raag_Identification/static/intrf/predf.png')
        img = plt.imread('/home/ubuntu/raag-identification/Raag_Identification/static/intrf/predf.png')
        plt.close('all')
        data=[]
        data.append(img[:,:,:3])
        print(img[:,:,:3].shape,'image shape after png')
        dat = np.array(data)
        
        cnn = Sequential()
        cnn.add(Conv2D(50, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu', input_shape=(432, 504, 3)))
        cnn.add(Conv2D(75, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(MaxPool2D(pool_size=(2,2)))
        cnn.add(Dropout(0.25))
        cnn.add(Conv2D(105, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(MaxPool2D(pool_size=(2,2)))
        cnn.add(Dropout(0.25))
        cnn.add(Conv2D(150, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(MaxPool2D(pool_size=(2,2)))
        cnn.add(Dropout(0.25))
        cnn.add(Conv2D(190, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(Dropout(0.25))
        cnn.add(Conv2D(240, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(Conv2D(300, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(Conv2D(330, kernel_size=(3,3), strides=(3,3), padding='same', activation='relu'))
        cnn.add(Dropout(0.25))
        cnn.add(GlobalAveragePooling2D())
        cnn.add(Dense(150, activation='relu'))
        cnn.add(Dropout(0.4))
        cnn.add(Dense(80, activation='relu'))
        cnn.add(Dropout(0.3))
        cnn.add(Dense(5, activation='softmax'))
        
        cnn.load_weights('/home/ubuntu/raag-identification/Raag_Identification/static/intrf/5cls_cnn.hdf5')
        pred = cnn.predict(dat)
        
        p=[]
        for i in range(len(pred[0])):
            p.append(pred[0][i])
        
        labels = {0:'Alahiya Bilaval', 1:'Bhup', 2:'Malkauns', 3:'Miyan Malhar', 4:'Yaman Kalyan'}
        g = p.index(max(p))
        try:
            os.remove('/home/ubuntu/raag-identification/Raag_Identification/static/intrf/predf.jpg')
        except:
            pass
        return labels[g]
        
