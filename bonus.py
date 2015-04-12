import sfml as sf
from random import randint
from collisions import Collidable
from obstacle import ObstacleLine
import utils
size = 50
spawn_time = 2


class BonusType(object):
    LIFE = "life"
    IMMORTALITY = "immortality"
    BULLET = "bullet"

IMMORTAL_TIME = 2


bonus_types = [BonusType.IMMORTALITY, BonusType.BULLET]


class BonusManager(object):
    def __init__(self, window, textures, collision_manager):
        self.textures = textures
        self.window = window
        self.spawned = []
        self.timer = 0
        self.collision_manager = collision_manager

    def update(self, delta_time):
        self.timer += delta_time
        if self.timer > spawn_time:
            btype = bonus_types[randint(0, len(bonus_types) - 1)]
            bonus = Bonus(self.textures[btype], btype, self.window)
            self.collision_manager.add(bonus)
            self.spawned.append(bonus)
            self.timer = 0

    def render(self, window):
        for bonus in self.spawned:
            bonus.render(window)


class Bonus(Collidable):

    def __init__(self, texture, btype, window):
        self.type = btype
        self.texture = texture
        self.not_collected = True
        self.position = randint(300, window.width - 300), randint(100, window.height - 100)
        self.sprite = utils.create_sprite(self.texture, size, size, self.position)

    def collide(self, other):
        if not isinstance(other, ObstacleLine) and not isinstance(other, Bonus):
            self.not_collected = False

    def get_bounding_rects(self):
        if self.not_collected:
            p = sf.Vector2(self.position[0], self.position[1])
            s = sf.Vector2(size, size)
            return sf.Rectangle((p.x - s.x / 2, p.y - s.y / 2), (s.x, s.y))

    def render(self, window):
        if self.not_collected:
            window.draw(self.sprite)





