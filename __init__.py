from mycroft import MycroftSkill, intent_file_handler
from mycroft.util import play_wav
import os
import wave
import struct
import math
import time


class SoundTuner(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        # https://www.seventhstring.com/resources/notefrequencies.html
        self.NOTES = {'C': 261.6,
                      'C#': 277.2,
                      'D': 293.7,
                      'D#': 311.1,
                      'E': 329.6,
                      'F': 349.2,
                      'F#': 370.0,
                      'G': 392.0,
                      'G#': 415.3,
                      'A': 440.0,
                      'A#': 466.2,
                      'B': 493.9}

    @intent_file_handler('tuner.sound.intent')
    def handle_tuner_sound(self, message):
        response = {'note': message.data.get("note")}
        if self.NOTES[message.data.get("note")]:
            self.speak_dialog('tuner.sound', data=response, wait=True)
            self.make_sound(message.data.get("note"))
        else:
            self.speak_dialog('can_not_do.sound', data=response, wait=True)

    def make_sound(self, note):
        sampleRate = 44100.0  # hertz
        duration = 2.0        # seconds
        frequency = self.NOTES[note]

        wavef = wave.open('sound.wav', 'w')
        wavef.setnchannels(1)  # mono
        wavef.setsampwidth(2)
        wavef.setframerate(sampleRate)

        for i in range(int(duration * sampleRate)):
            value = int(32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate)))
            data = struct.pack('<h', value)
            wavef.writeframesraw(data)

        wavef.close()
        play_wav('sound.wav',)
        time.sleep(2)
        os.remove('sound.wav')





def create_skill():
    return SoundTuner()

