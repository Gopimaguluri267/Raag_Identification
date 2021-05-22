import librosa
import scipy
from scipy.io.wavfile import write

class convert():
    def to_wav(self, x):
        samples, sampling_rate = librosa.load(x)
        scipy.io.wavfile.write('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/new_sample.wav', sampling_rate, samples)
        return None
