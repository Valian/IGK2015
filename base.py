import sfml as sf
from collisions import Collidable
import utils
tile_width = 20


class Base(Collidable):
    def get_bounding_rects(self):
        return [t.global_bounds for t in self.life_tiles]

    def collide(self, other):
        self.hit(other.plane.position.y)

    def __init__(self, id, lives, red_texture, green_texture, window_height, window_width):
        self.red_texture = red_texture
        self.green_texture = green_texture
        self.lives = lives
        self.id = id
        self.life_tiles = self.create_life_tiles(window_height, window_width)

    def create_life_tiles(self, window_height, window_width):
        tile_height = window_height * 1.0 / self.lives
        tile_x_pos = 0 if self.id == 'left' else window_width - tile_width
        tile_y_pos = 0
        sprites = []
        for i in xrange(self.lives):
            rect = sf.Rectangle((tile_x_pos, tile_y_pos), (tile_width, tile_height))
            sprites.append(utils.create_sprite(self.green_texture, rect.width, rect.height, rect.position))
            tile_y_pos += tile_height
        return sprites

    def render(self, window):
        for sprite in self.life_tiles:
            window.draw(sprite)

    def hit(self, hitpoint):
        self.lives -= 1
        for tile in self.life_tiles:
            if tile.local_bounds.position.y <= hitpoint <= tile.local_bounds.position.y + tile.local_bounds.height:
                tile.texture = self.red_texture
                break



