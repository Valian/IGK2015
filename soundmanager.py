import sfml as sf


class SoundManager():
    def __init__(self):
        self.sounds = self.init_sound()
        pass

    def init_sound(self):
        return {'music': sf.Music.from_file('assets/music/music.wav')}

    def play_background_music(self):
        bmusic = self.sounds['music']
        bmusic.loop = True
        bmusic.play()
