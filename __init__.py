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
        self.NOTES = {'C middle': 261.6,
                      'C': 261.6,
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
                      'B': 493.9,
                      'C0': 16.35,
                      'C#0': 17.32,
                      'D0': 18.35,
                      'D#0': 19.45,
                      'E0': 20.60,
                      'F0': 21.83,
                      'F#0': 23.12,
                      'G0': 24.50,
                      'G#0': 25.96,
                      'A0': 27.50,
                      'A#0': 29.14,
                      'B0': 30.87,
                      'C1': 32.70,
                      'C#1': 34.65,
                      'D1':	36.71,
                      'D#1': 38.89,
                      'E1':	41.20,
                      'F1':	43.65,
                      'F#1': 46.25,
                      'G1':	49.00,
                      'G#1': 51.91,
                      'A1':	55.00,
                      'A#1': 58.27,
                      'B1':	61.74,
                      'C2': 65.41,
                      'C#2': 69.30,
                      'D2':	73.42,
                      'D#2': 77.78,
                      'E2':	82.41,
                      'F2':	87.31,
                      'F#2': 92.50,
                      'G2':	98.00,
                      'G#2': 103.8,
                      'A2':	110.0,
                      'A#2': 116.5,
                      'B2': 123.5,
                      'C3': 130.8,
                      'C#3': 138.6,
                      'D3':	146.8,
                      'D#3': 155.6,
                      'E3':	164.8,
                      'F3':	174.6,
                      'F#3': 185.0,
                      'G3':	196.0,
                      'G#3': 207.7,
                      'A3':	220.0,
                      'A#3': 233.1,
                      'B3': 246.9,
                      'C4': 261.6,
                      'C#4': 277.2,
                      'D4': 293.7,
                      'D#4': 311.1,
                      'E4': 329.6,
                      'F4': 349.2,
                      'F#4': 370.0,
                      'G4': 392.0,
                      'G#4': 415.3,
                      'A4': 440.0,
                      'A#4': 466.2,
                      'B4': 493.9,
                      'C5': 523.3,
                      'C#5': 554.4,
                      'D5': 587.3,
                      'D#5': 622.3,
                      'E5':	659.3,
                      'F5':	698.5,
                      'F#5': 740.0,
                      'G5':	784.0,
                      'G#5': 830.6,
                      'A5':	880.0,
                      'A#5': 932.3,
                      'B5':	987.8,
                      'C6': 1047,
                      'C#6': 1109,
                      'D6': 1175,
                      'D#6': 1245,
                      'E6': 1319,
                      'F6':	1397,
                      'F#6': 1480,
                      'G6':	1568,
                      'G#6': 1661,
                      'A6': 1760,
                      'A#6': 1865,
                      'B6':	1976
                      }

        self.GUITAR = {'Low E': 'E2',
                       'A': 'A3',
                       'D': 'D4',
                       'G': 'G4',
                       'B': 'B4',
                       'High E': 'E5'
                       }

    @intent_file_handler('tuner.sound.intent')
    def handle_tuner_sound(self, message):
        response = {'note': message.data.get("note")}
        try:
            if self.NOTES[message.data.get("note")]:
                self.speak_dialog('tuner.sound', data=response, wait=False)
                self.make_sound(message.data.get("note"))
        except Exception:
            self.speak_dialog('can_not_do', data=response, wait=False)

    @intent_file_handler('guitar.intent')
    def handle_guitar(self, message):
        response = {'string': message.data.get("string")}
        try:
            if self.GUITAR[message.data.get("string")]:
                self.speak_dialog('guitar', data=response, wait=False)
                string = self.GUITAR[message.data.get("string")]
                self.make_sound(string)
        except Exception:
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
