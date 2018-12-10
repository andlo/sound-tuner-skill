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
        name = lambda n: labels[n%len(labels)] + str(int((n+(9+4*12))/12))
        # the frequency of a note. the parameter n is the number of half-tones
        # from a4, which has a frequency of 440Hz, and is our reference note.
        freq   = lambda n: int(440*(math.pow(2,1/12)**n))
        # a dictionnary associating note frequencies to note names
        self.NOTES = {name(n): freq(n) for n in range(-42, 60)}

        # Guitar strings are E2=82.41Hz, A2=110Hz, D3=146.8Hz, G3=196Hz, B3=246.9Hz, E4=329.6Hz
        # Bass strings are (5th string) B0=30.87Hz, (4th string) E1=41.20Hz, A1=55Hz, D2=73.42Hz, G2=98Hz
        # Mandolin & violin strings are G3=196Hz, D4=293.7Hz, A4=440Hz, E5=659.3Hz
        # Viola & tenor banjo strings are C3=130.8Hz, G3=196Hz, D4=293.7Hz, A4=440Hz
        # Cello strings are C2=65.41Hz, G2=98Hz, D3=146.8Hz, A3=220Hz

        self.GUITAR = {'LOW E': 'E2',
                       'A': 'A2',
                       'D': 'D3',
                       'G': 'G3',
                       'B': 'B3',
                       'HIGH E': 'E4'
                       }
        self.INSTRUMENT = {
            'GUITAR': {'LOW E': 'E2', 'A': 'A2', 'D': 'D3', 'G': 'G3','B': 'B3', 'HIGH E': 'E4'},
            'MANDOLIN': {'G': 'G3', 'D': 'D4', 'A': 'A4', 'E': 'E5'},
            'VIOLIN': {'G': 'G3', 'D': 'D4', 'A': 'A4', 'E': 'E5'},
            'CELLO': {'C': 'C2', 'G': 'G2', 'D': 'D3', 'A': 'A3'},
            'VIOLA': {'C': 'C3', 'G': 'G3', 'D': 'D4', 'A': 'A4'},
            'BANJO': {'C': 'C3', 'G': 'G3', 'D': 'D4', 'A': 'A4'},
            'BASS': {'B': 'B0', 'E': 'E1', 'A': 'A1', 'D': 'D2', 'G': 'G2'}}


    @intent_file_handler('tuner.sound.intent')
    def handle_tuner_sound(self, message):
        message = str.upper(message.data.get("note"))
        response = {'note': message}
        if self.NOTES.get(message):
            self.speak_dialog('tuner.sound', data=response, wait=False)
            self.make_sound(message)
        elif self.NOTES.get(message + '4'):
            self.speak_dialog('tuner.sound', data=response, wait=False)
            self.make_sound(message + '4')
        else:
            self.speak_dialog('can_not_do', data=response, wait=False)

    @intent_file_handler('instrument.intent')
    def handle_instrument(self, message):
        instrument = str.upper(message.data.get("instrument"))
        string = str.upper(message.data.get("string"))
        response = {'instrument': instrument, 'string': string}

        if self.INSTRUMENT.get(instrument):
            instrument2 = self.INSTRUMENT.get(instrument)
            if instrument2.get(string):
                self.speak_dialog('instrument', data=response, wait=False)
                string2 = instrument2[string]
                self.make_sound(string2)
            else:
                self.speak_dialog('can_not_do_instrument', data=response, wait=False)
        else:
            self.speak_dialog('can_not_do_instrument', data=response, wait=False)

    def make_sound(self, note):
        sampleRate = 48000.0  # hertz
        duration = 2.0
        frequency = self.NOTES[note]

        wavef = wave.open('/tmp/sound.wav', 'w')
        wavef.setnchannels(1)  # mono
        wavef.setsampwidth(2)
        wavef.setframerate(sampleRate)

        for i in range(int(duration * sampleRate)):
            value = int(32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate)))
            data = struct.pack('<h', value)
            wavef.writeframesraw(data)

        wavef.close()
        play_wav('/tmp/sound.wav')
        time.sleep(duration)
        os.remove('/tmp/sound.wav')


def create_skill():
    return SoundTuner()
