import numpy as np 
import matplotlib.pyplot as plt
from pydub import AudioSegment
import librosa
import librosa.display 
import parselmouth

class RaagAnalysis():
    def MelSpec_Pitch(self, x):
        samples, sampling_rate = librosa.load(x)
        m = librosa.feature.melspectrogram(samples, sr=sampling_rate, n_mels=128)
        log_m = librosa.power_to_db(m, ref=np.max)
        song=parselmouth.Sound(x)
        pitch=song.to_pitch()
        pitch_values=pitch.selected_array['frequency']
        pitch_values[pitch_values==0]=np.nan
        plt.figure(figsize=(17,8))
        librosa.display.specshow(log_m, sr=sampling_rate, x_axis='time', y_axis='mel')
        plt.plot(pitch.xs(), pitch_values, linewidth=2, color='black')
        plt.xlim([song.xmin, song.xmax])
        plt.title('Mel Spectrogram and Pitch Contour overlapped')
        plt.xlabel('Time [seconds]')
        plt.ylabel('Frequency_Mel scale [Hz]')
        # t='.jpg'
        # name=x[:-4]+t
        # name='tempPlot'+t
        plt.savefig('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/tempPlot.png')
        img = plt.imread('/home/ubuntu/raag-identification/Raag_Identification/static/uploads/tempPlot.png')
        plt.close('all')
        return img

# rg = RaagAnalysis()
# rg.MelSpec_Pitch("C:/Users/Gopi Maguluri/Raag Identification and Understanding/FRIU/static/uploads/Malkauns_JaakoManaRaam_med.wav")
