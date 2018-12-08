from mycroft import MycroftSkill, intent_file_handler


class SoundTuner(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('tuner.sound.intent')
    def handle_tuner_sound(self, message):
        self.speak_dialog('tuner.sound')


def create_skill():
    return SoundTuner()

