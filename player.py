import sfml as sf
import random
from animation import Animation, AnimatedSprite
from bonus import Bonus, BonusType, IMMORTAL_TIME
from shot import Bullet
from soundmanager import Instance as SoundManager
from collisions import Collidable
from obstacle import ObstacleLine


LEFT_SIDE = 1
RIGHT_SIDE = 2

PADDING = 50

GRAVITY = 20.0


class PlayerManager(object):

    def __init__(self, window_size, distance_from_base, first_player_tex, second_player_tex, speed):
        self.window_rect = sf.Rectangle((0, 0), (window_size.x, window_size.y))
        self.speed = speed
        self.first_player_tex = first_player_tex
        self.second_player_tex = second_player_tex
        self.left_pos = distance_from_base
        self.right_pos = window_size.x - distance_from_base
        self.min_y = PADDING
        self.max_y = window_size.y - PADDING

        self.players_by_key = {}

    def handle_event(self, event, collision_manager):
        if not isinstance(event, sf.KeyEvent):
            return

        player = self.players_by_key.get(event.code)
        if player:
            player.jump()
        else:
            self.create_player(event.code, collision_manager)

    def create_player(self, key, collision_manager):
        side = 1 if len(self.players_by_key) % 2 == 0 else -1
        tex = self.first_player_tex if len(self.players_by_key) % 2 == 0 else self.second_player_tex
        starting_pos = (self.left_pos if side > 0 else self.right_pos, random.randint(self.min_y, self.max_y))
        self.players_by_key[key] = Player(self.speed * side, starting_pos, tex, self.window_rect, collision_manager)
        collision_manager.add(self.players_by_key[key])

    def update(self, elapsed_time):
        for key, player in self.players_by_key.iteritems():
            player.update(elapsed_time)

    def render(self, window):
        for player in self.players_by_key.values():
            player.render(window)


class Player(Collidable):

    def __init__(self, speed, starting_position, texture, window_rectangle, collision_manager):
        self.window_rectangle = window_rectangle
        self.starting_position = starting_position
        self.speed = speed
        self.collision_manager = collision_manager
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
        self.plane.size = sf.Vector2(self.plane.global_bounds.width / 2, self.plane.global_bounds.height / 2)
        self.plane.origin = self.plane.global_bounds.width / 2.0, self.plane.global_bounds.height / 2.0
        self.plane.scale((self.direction * 0.5, 0.5))

        self.plane.position = self.starting_position
        self.plane_speed = sf.Vector2(speed, 0)

        self.is_dead = False
        self.jump_time = None
        self.plane_jumped = False

        self.immortal = None

        self.bullets = set()

        SoundManager.play_player_appear_sound()

    def get_bounding_rects(self):
        if not self.is_dead:
            p = self.plane.position
            s = self.plane.size
            return sf.Rectangle((p.x - s.x / 3, p.y - s.y / 3), (s.x / 1.5, s.y/1.5))

    def collide(self, other):
        if isinstance(other, ObstacleLine) or (isinstance(other, Player) and self.direction != other.direction):
            if self.immortal:
                return

            if not isinstance(other, ObstacleLine):
                SoundManager.play_death_sound()
            self.reset()
        elif isinstance(other, Bonus):
            if other.type == BonusType.IMMORTALITY:
                self.immortal = sf.Clock()
                self.plane.color = sf.Color(255, 255, 255)
            elif other.type == BonusType.BULLET:
                bullet = Bullet(self.plane.position, self.speed * 2)
                self.collision_manager.add(bullet)
                self.bullets.add(bullet)
        elif isinstance(other, Bullet):
            if self.immortal or not other.alive:
                return
            SoundManager.play_death_sound()
            self.reset()

    def jump(self):
        if self.is_dead:
            self.is_dead = False
            SoundManager.play_player_appear_sound()

        if not self.plane_jumped:
            self.plane_jumped = True
            self.jump_time = sf.Clock()

    def render(self, window):
        if not self.is_dead:
            window.draw(self.plane)
        for bullet in self.bullets:
            bullet.render(window)

    def reset(self):
        self.plane.position = self.starting_position
        self.plane_speed = sf.Vector2(self.speed, 0)

        self.is_dead = True
        self.jump_time = None
        self.plane_jumped = False
        self.plane.rotation = 0
        self.immortal = None

    def update(self, elapsed_time):
        for bullet in self.bullets:
            bullet.update(elapsed_time)



        self.check_bounds()

        if self.is_dead:
            return

        if not self.plane_jumped and (self.plane.rotation <= 60 or self.plane.rotation >= 300):
            self.plane.rotate(1.25 * self.direction)

        if self.immortal and self.immortal.elapsed_time.seconds > IMMORTAL_TIME:
            self.immortal = None
            self.plane.color = sf.Color(255, 255, 255, 255)

        if self.plane_jumped:
            self.plane_speed.y = -200.0

            if self.jump_time.elapsed_time.seconds < 0.25:
                self.plane.rotate(-2.5 * self.direction)
            else:
                self.plane_jumped = False
                self.jump_time = None
            if self.plane.rotation % 300 > 60:
                self.plane.rotation = (300, 60)[self.plane.rotation * self.direction > 300]

        if self.plane_speed.y <= 50 * GRAVITY:
            self.plane_speed += sf.Vector2(0.0, GRAVITY)

        self.plane.move(self.plane_speed * elapsed_time)
        self.plane.update(sf.seconds(elapsed_time))

    def check_bounds(self):
        if not self.window_rectangle.contains(self.plane.position):
            SoundManager.play_death_sound()
            self.reset()

