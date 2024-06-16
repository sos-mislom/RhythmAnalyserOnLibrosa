import librosa
import numpy as np
import json
import random
def analyze_song(file_path):
    y, sr = librosa.load(file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    extended = []
    
    for beat in  beat_times.tolist():
        extended.append(beat)
        num_additional_beats = random.randint(1, 2)
        for _ in range(num_additional_beats):
            extended.append(beat + 0.1)
        
    analysis_data = {
        'tempo': float(tempo),
        'beats': extended
    }
    
    with open('song_analysis.json', 'w') as json_file:
        json.dump(analysis_data, json_file)

    print(f'Анализ завершен. Темп: {tempo:.2f} BPM')
    print(f'Результаты сохранены в song_analysis.json')

analyze_song(r'C:\Users\User\Desktop\audio.mp3')
