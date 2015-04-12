import sfml as sf
from random import randint
from collisions import Collidable
import utils
size = 50
spawn_time = 2


class BonusType(object):
    LIFE = "life"
    IMMORTALITY = "immortality"
    BULLET = "bullet"

bonus_types = [BonusType.LIFE, BonusType.BULLET, BonusType.IMMORTALITY]


class BonusManager(object):
    def __init__(self, window, textures):
        self.textures = textures
        self.window = window
        self.spawned = []
        self.timer = 0

    def update(self, delta_time):
        self.timer += delta_time
        if self.timer > spawn_time:
            btype = bonus_types[randint(0, len(bonus_types) - 1)]
            self.spawned.append(Bonus(self.textures[btype], btype, self.window))
            self.timer = 0


    def render(self, window):
        for bonus in self.spawned:
            window.draw(bonus.sprite)


class Bonus(Collidable):
    def collide(self, other):
        pass

    def get_bounding_rects(self):
        pass

    def __init__(self, texture, btype, window):
        self.type = btype
        self.texture = texture
        self.sprite = utils.create_sprite(self.texture, size, size,
                                    (randint(300, window.width - 300), randint(100, window.height - 100)))





