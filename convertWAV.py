import librosa
import scipy
from scipy.io.wavfile import write

class convert():
    def to_wav(self, x):
        samples, sampling_rate = librosa.load(x)
        scipy.io.wavfile.write('C:/Users/Gopi Maguluri/Raag Identification and Understanding/FRIU/static/uploads/new_sample.wav', sampling_rate, samples)
        return None