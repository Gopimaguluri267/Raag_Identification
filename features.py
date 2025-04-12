import numpy as np 
import matplotlib.pyplot as plt
from pydub import AudioSegment
import librosa
import librosa.display 
# import parselmouth
import os
import config

class RaagAnalysis():
    def MelSpec_Pitch(self, x):
        samples, sampling_rate = librosa.load(x)
        m = librosa.feature.melspectrogram(y=samples, sr=sampling_rate, n_mels=128)
        log_m = librosa.power_to_db(m, ref=np.max)
        # song=parselmouth.Sound(x)
        # pitch=song.to_pitch()
        # pitch_values=pitch.selected_array['frequency']
        # pitch_values[pitch_values==0]=np.nan
        # Extract pitch using librosa
        pitches, magnitudes = librosa.piptrack(y=samples, sr=sampling_rate)
        
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch_values.append(pitches[index, t])
        
        times = librosa.times_like(np.array(pitch_values))
        
        plt.figure(figsize=(17,8))
        librosa.display.specshow(log_m, sr=sampling_rate, x_axis='time', y_axis='mel')
        # plt.plot(pitch.xs(), pitch_values, linewidth=2, color='black')
        # plt.xlim([song.xmin, song.xmax])
        plt.plot(times, pitch_values, linewidth=2, color='white', alpha=0.9, label='Pitch Contour')
        plt.title('Mel Spectrogram and Pitch Contour overlapped')
        plt.xlabel('Time [seconds]')
        plt.ylabel('Frequency_Mel scale [Hz]')
        plt.legend()
        plt.tight_layout()        
        plt.savefig(os.path.join(config.UPLOAD_FOLDER, 'tempPlot.jpg'))
        img = plt.imread(os.path.join(config.UPLOAD_FOLDER, 'tempPlot.jpg'))
        return img
