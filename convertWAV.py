import librosa
import scipy
from scipy.io.wavfile import write
import os
import config

class convert():
    def to_wav(self, x):
        samples, sampling_rate = librosa.load(x)
        scipy.io.wavfile.write(os.path.join(config.UPLOAD_FOLDER, 'new_sample.wav'), sampling_rate, samples)
        return None
