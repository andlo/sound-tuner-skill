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
        labels = ['A','A#','B','C','C#','D','D#','E','F','E#','G','G#']
        # name is the complete name of a note (label + octave). the parameter
        # n is the number of half-tone from A4 (e.g. D#1 is -42, A3 is -12, A5 is 12)
        name   = lambda n: labels[n%len(labels)] + str(int((n+(9+4*12))/12))
        # the frequency of a note. the parameter n is the number of half-tones
        # from a4, which has a frequency of 440Hz, and is our reference note.
        freq   = lambda n: int(440*(math.pow(2,1/12)**n))
        # a dictionnary associating note frequencies to note names
        self.NOTES = {name(n): freq(n) for n in range(-42,60)}

        self.GUITAR = {'Low E': 'E2',
                       'A': 'A2',
                       'D': 'D3',
                       'G': 'G3',
                       'B': 'B3',
                       'High E': 'E4'
                       }

    @intent_file_handler('tuner.sound.intent')
    def handle_tuner_sound(self, message):
        response = {'note': message.data.get("note")}
        if self.NOTES.get(message.data.get("note")):
            self.speak_dialog('tuner.sound', data=response, wait=False)
            self.make_sound(message.data.get("note"))
        elif self.NOTES.get(message.data.get("note") + '4'):
            self.speak_dialog('tuner.sound', data=response, wait=False)
            self.make_sound(message.data.get("note") + '4')
        else:
            self.speak_dialog('can_not_do', data=response, wait=False)

    @intent_file_handler('guitar.intent')
    def handle_guitar(self, message):
        response = {'string': message.data.get("string")}
        if self.GUITAR.get(message.data.get("string")):
            self.speak_dialog('guitar', data=response, wait=False)
            string = self.GUITAR[message.data.get("string")]
            self.make_sound(string)
        else:
            self.speak_dialog('can_not_do', data=response, wait=False)

    def make_sound(self, note):
        sampleRate = 48000.0  # hertz
        duration = 2.0
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
        play_wav('sound.wav')
        time.sleep(duration)
        os.remove('sound.wav')


def create_skill():
    return SoundTuner()
