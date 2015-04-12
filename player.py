import sfml as sf
import random
from matplotlib.mlab import distances_along_curve
from animation import Animation, AnimatedSprite


LEFT_SIDE = 1
RIGHT_SIDE = 2

PADDING = 50

GRAVITY = 10.0


class PlayerManager(object):

    def __init__(self, window_size, distance_from_base, texture, speed):
        self.speed = speed
        self.texture = texture
        self.left_pos = distance_from_base
        self.right_pos = window_size.x - distance_from_base
        self.min_y = PADDING
        self.max_y = window_size.y - PADDING

        self.players_by_key = {}

    def handle_event(self, event):
        if not isinstance(event, sf.KeyEvent):
            return

        player = self.players_by_key.get(event.code)
        if player:
            player.jump()
        else:
            self.create_player(event.code)

    def create_player(self, key):
        side = 1 if len(self.players_by_key) % 2 == 0 else -1
        starting_pos = (self.left_pos if side > 0 else self.right_pos, random.randint(self.min_y, self.max_y))
        self.players_by_key[key] = Player(self.speed * side, starting_pos, self.texture)

    def update(self, elapsed_time):
        for key, player in self.players_by_key.iteritems():
            player.update(elapsed_time)

    def render(self, window):
        for player in self.players_by_key.values():
            player.render(window)


class Player(object):

    def __init__(self, speed, starting_position, texture):
        self.starting_position = starting_position
        self.speed = speed
        self.direction = 1 if speed > 0 else -1

        # Plane
        fly_anim = Animation()
        fly_anim.texture = texture
        fly_anim.add_frame(sf.Rectangle((0, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((88, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((176, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((88, 0), (88, 73)))

        self.plane = AnimatedSprite(sf.seconds(0.2), False, True)
        self.plane.play(fly_anim)
        self.plane.origin = self.plane.global_bounds.width / 2.0, self.plane.global_bounds.height / 2.0
        self.plane.scale((self.direction, 1))

        self.plane.position = starting_position

        self.plane_speed = sf.Vector2(speed, 0)

        self.jump_time = None
        self.plane_jumped = False

    def jump(self):
        if not self.plane_jumped:
            self.plane_jumped = True
            self.jump_time = sf.Clock()

    def render(self, window):
        window.draw(self.plane)

    def update(self, elapsed_time):
        # Plane
        if not self.plane_jumped and (self.plane.rotation <= 60 or self.plane.rotation >= 300):
            self.plane.rotate(1.25)

        if self.plane_jumped:
            self.plane_speed.y = -150.0

            if self.jump_time.elapsed_time.seconds < 0.25:
                self.plane.rotate(-2.5 * self.direction)
            else:
                self.plane_jumped = False
                self.jump_time = None
            if self.plane.rotation * self.direction % 300 > 60:
                self.plane.rotation = (300, 60)[self.plane.rotation * self.direction > 300]

        if self.plane_speed.y <= 50 * GRAVITY:
            self.plane_speed += sf.Vector2(0.0, GRAVITY)

        self.plane.move(self.plane_speed * elapsed_time)
        self.plane.update(sf.seconds(elapsed_time))
