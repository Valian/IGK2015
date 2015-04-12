from collisions import Collidable
import sfml as sf
from soundmanager import Instance as SoundManager
from utils import create_sprite

_bullet_tex = sf.Texture.from_file("assets/images/bullet.png")
window_rectangle = sf.Rectangle((0, 0), (1200, 750))


class Bullet(Collidable):

    def get_bounding_rects(self):
        if self.alive:
            p = self.sprite.position
            s = sf.Vector2(20, 20)
            return sf.Rectangle((p.x - s.x / 2, p.y - s.y / 2), (s.x, s.y))

    def collide(self, other):
        if isinstance(other, Bullet):
            return

        if hasattr(other, 'plane') and other.speed * self.speed < 0:
            SoundManager.play_explosion_sound()
            self.alive = False

        if not hasattr(other, 'plane'):
            SoundManager.play_explosion_sound()
            self.alive = False

    def __init__(self, position, speed):
        self.speed = speed
        self.position = position
        self.sprite = create_sprite(_bullet_tex, 20, 20, self.position)
        self.alive = True

    def update(self, elapsed_time):
        self.sprite.move(sf.Vector2(self.speed, 0) * elapsed_time)

        if not window_rectangle.contains(self.sprite.position):
            #SoundManager.play_explosion_sound()
            self.alive = False

    def render(self, window):
        if self.alive:
            window.draw(self.sprite)

