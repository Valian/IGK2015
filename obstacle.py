from random import randint
import sfml as sf
import utils

maxFragCount = 10
minFragCount = 4
minRectHeight = 200
maxRectHeight = 300
minSpace = 50
maxSpace = 100
start_y_position = -100
end_y_position_offset = 100

class ObstacleLine(object):
    def __init__(self, speed, width, position, texture):
        self.fragCount = randint(minFragCount, maxFragCount)
        self.xPosition = position
        self.texture = texture
        self.frag_speed = speed
        self.rectWidth = width
        self.obstacles = [utils.create_sprite(self.texture, rect.width, rect.height, rect.position) for rect in self.create_fragments()]

    def update(self, window_height, deltatime):
        for i in range(0, len(self.obstacles)):
            self.obstacles[i].move(sf.Vector2(0, self.frag_speed * deltatime))
            if self.obstacles[i].position.y > window_height:
                self.obstacles[i].position = (self.xPosition,
                                              self.obstacles[i + 1 if i < len(self.obstacles) - 1 else 0].position.y - self.obstacles[i].local_bounds.height - randint(minSpace, maxSpace))

    def render(self, window):
        for sprite in self.obstacles:
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