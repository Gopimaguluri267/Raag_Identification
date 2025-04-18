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
import config
from PIL import Image

class raag_pred():
    def pred(self, x):
        samples, sampling_rate = librosa.load(x)
        stft = np.abs(librosa.stft(samples))**2
        M = librosa.feature.melspectrogram(S=stft)
        M = librosa.feature.melspectrogram(y=samples, sr=sampling_rate, n_mels=128, fmax=8000)
        log_M = librosa.power_to_db(M, ref=np.max)
        plt.figure(figsize=(4.32, 5.04))
        plt.subplot(2, 1, 1)
        librosa.display.specshow(log_M, y_axis='mel', fmax=8000, x_axis='time')
        plt.tight_layout()
        plt.savefig(os.path.join(config.INTERMEDIATE_FILES_FOLDER, 'predf.jpg'), dpi=100, bbox_inches='tight')
        
        img_path = os.path.join(config.INTERMEDIATE_FILES_FOLDER, 'predf.jpg')
        img = Image.open(img_path)
        img = img.resize((504, 432))
        img.save(img_path)
        img = plt.imread(img_path)
        
        data=[]
        data.append(img)
        dat = np.array(data)
        
        print(f"Input shape to model: {dat.shape}")
        
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
        
        cnn.load_weights(os.path.join(config.INTERMEDIATE_FILES_FOLDER, '5cls_cnn.hdf5'))
        pred = cnn.predict(dat)
        
        p=[]
        for i in range(len(pred[0])):
            p.append(pred[0][i])
        
        labels = {0:'Alahiya Bilaval', 1:'Bhup', 2:'Malkauns', 3:'Miyan Malhar', 4:'Yaman Kalyan'}
        g = p.index(max(p))
        return labels[g]
        