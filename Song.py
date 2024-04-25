from collections import Counter
import librosa
import numpy as np

from Helpers import PATH

class Song(object):
    def __init__(self, path):
        self.tempo = None
        self.beats = None
        self.times = None
        self.path = path
        self.analyze()

    def analyze(self):
        y, sr = librosa.load(self.path)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env)
        self.tempo = tempo
        self.beats = beats
        self.times = list(librosa.frames_to_time(beats, sr=sr))

    def getTempo(self):
        return self.tempo

    def getBeatFrames(self):
        return self.beats

    def getBeatTimes(self):
        return self.times

    def getPath(self):
        return self.path
    @staticmethod
    def main():
        song = Song(PATH)


if __name__ == "__main__":
    Song.main()
