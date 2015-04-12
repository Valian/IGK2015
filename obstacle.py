from random import randint
import sfml as sf
from collisions import Collidable
import utils

maxFragCount = 10
minFragCount = 4
minRectHeight = 200
maxRectHeight = 300
minSpace = 50
maxSpace = 100
start_y_position = -100
end_y_position_offset = 100


class ObstacleLine(Collidable):
    def get_bounding_rects(self):
        for obs, rect in self.obstacles:
            yield sf.Rectangle((obs.position.x, obs.position.y), (rect.size.x, rect.size.y))

    def collide(self, other):
        pass

    def __init__(self, speed, width, position, texture):
        self.fragCount = randint(minFragCount, maxFragCount)
        self.xPosition = position
        self.texture = texture
        self.frag_speed = speed
        self.rectWidth = width
        self.obstacles = [(utils.create_sprite(self.texture, rect.width, rect.height, rect.position), rect) for rect in self.create_fragments()]

    def update(self, window_height, deltatime):
        for i in range(0, len(self.obstacles)):
            obstacle = self.obstacles[i][0]
            obstacle.move(sf.Vector2(0, self.frag_speed * deltatime))
            if obstacle.position.y > window_height:
                obstacle.position = (self.xPosition,
                                              self.obstacles[i + 1 if i < len(self.obstacles) - 1 else 0][0].position.y - obstacle.local_bounds.height - randint(minSpace, maxSpace))

    def render(self, window):
        for sprite, rect in self.obstacles:
            window.draw(sprite)

    def create_fragments(self):
        ypos = start_y_position
        for i in range(0, self.fragCount):
            rect = self.create_random_fragment(ypos)
            ypos += rect.height
            ypos += randint(minSpace, maxSpace)
            yield rect

    def create_random_fragment(self, ypos):
        return sf.Rectangle((self.xPosition, ypos), (self.rectWidth, randint(minRectHeight, maxRectHeight)))