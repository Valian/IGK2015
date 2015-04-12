import sfml as sf


class SoundManager():
    def __init__(self):
        self.sounds = self.init_sound()
        pass

    def init_sound(self):
        return {'music': sf.Music.from_file('assets/music/music.wav'),
            'plop': sf.Music.from_file('assets/music/plop.wav'),
            'death': sf.Music.from_file('assets/music/death.wav'),
            'expl': sf.Music.from_file('assets/music/expl.wav')}

    def play_background_music(self):
        bmusic = self.sounds['music']
        bmusic.loop = True
        bmusic.play()

    def play_death_sound(self):
        self.sounds['death'].play()

    def play_player_appear_sound(self):
        self.sounds['plop'].play()

    def play_explosion_sound(self):
        self.sounds['expl'].play()

Instance = SoundManager()

