from random import randint
import sfml as sf
import utils

maxFragCount = 5
rectWidth = 50
minRectHeight = 50
maxRectHeight = 100
minSpace = 40
maxSpace = 60
frag_speed = 10
start_y_position = -100
end_y_position_offset = 100

class ObstacleLine(object):
    def __init__(self, speed, width, position):
        self.fragCount = randint(0, maxFragCount)
        self.xPosition = position
        self.obstacles = [utils.create_sprite(rect) for rect in self.create_fragments()]

    def update(self,window_height, deltatime):
        for i in range(0, len(self.obstacles)):
            self.obstacles[i].move(sf.Vector2(0, frag_speed * deltatime))
            if self.obstacles[i].top > window_height + end_y_position_offset:
                self.obstacles[i].top = start_y_position

    def render(self, window):
        for sprite in self.obstacles:
            window.draw(sprite)

    def create_fragments(self):
        obstacles = []
        ypos = start_y_position
        for i in range(0, self.fragCount):
            rect = self.create_random_fragment(ypos)
            self.obstacles.append(rect)
            ypos += rect.height
            ypos += randint(minSpace, maxSpace)
        return obstacles

    def create_random_fragment(self, ypos):
        return sf.Rectangle((self.xPosition, ypos), (rectWidth, randint(minRectHeight, maxRectHeight)))