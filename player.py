LEFT_SIDE = 1
RIGHT_SIDE = 2


class Player(object):

    def __init__(self, key, side, starting_position):
        self.starting_position = starting_position
        self.side = side
        self.key = key

    # Plane
        fly_anim = Animation()
        fly_anim.texture = self.plane_sheet
        fly_anim.add_frame(sf.Rectangle((0, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((88, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((176, 0), (88, 73)))
        fly_anim.add_frame(sf.Rectangle((88, 0), (88, 73)))

        self.plane = AnimatedSprite(sf.seconds(0.2), False, True)
        self.plane.play(fly_anim)
        self.plane.origin = self.plane.global_bounds.width / 2.0, self.plane.global_bounds.height / 2.0

        self.plane.position = sf.Vector2(150, 200)

        self.plane_speed = sf.Vector2(0.0, 0.0)

        self.jump_time = None

        self.plane_jumped = False


        if type(event) is sf.KeyEvent and event.code is sf.Keyboard.SPACE:
            self.plane_jumped = True
            self.jump_time = sf.Clock()

        # Plane
        if not self.plane_jumped and (self.plane.rotation <= 60 or self.plane.rotation >= 300):
            self.plane.rotate(1.25)

        if self.plane_jumped:
            self.plane_speed = sf.Vector2(0.0, -150.0)

            if self.jump_time.elapsed_time.seconds < 0.25:
                self.plane.rotate(-2.5)
            else:
                self.plane_jumped = False
                self.jump_time = None
            if self.plane.rotation % 300 > 60:
                self.plane.rotation = (300, 60)[self.plane.rotation > 300]

        if self.plane_speed.y <= 50 * GRAVITY:
            self.plane_speed += sf.Vector2(0.0, GRAVITY)

        self.plane.move(self.plane_speed * elapsed_time)
        self.plane.update(sf.seconds(elapsed_time))
