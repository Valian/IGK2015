#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf
import sys
from collisions import CollisionManager
from player import PlayerManager
from utils import *
from animation import *
from obstacle import ObstacleLine
from base import Base

WWIDTH, WHEIGHT = 1200, 750
WTITLE = "IGK 2015"
NUMBER_OF_OBSTACLES = 4
DIST_FROM_BASE = 100
SPEED = 800

SETTINGS = sf.ContextSettings()
SETTINGS.antialiasing_level = 8
GRAVITY = 10.0
LIVES = 10


class Game:
    def __init__(self):
        # Window
        self.window = sf.RenderWindow(sf.VideoMode(WWIDTH, WHEIGHT), WTITLE, sf.Style.CLOSE | sf.Style.TITLEBAR,
                                      SETTINGS)
        self.window.framerate_limit = 60

        # Clock
        self.clock = sf.Clock()

        # View
        self.view = sf.View(sf.Rectangle((0, 0), (WWIDTH, WHEIGHT)))
        self.window.view = self.view

        # Loading assets
        self.textures = self.load_assets()
        self.bg = create_sprite(self.textures['bg'], WWIDTH, WHEIGHT, (0, 0))

        self.collision_manager = CollisionManager()

        self.obstacles = self.create_obstacles()
        self.bases = self.create_bases()
        self.player_manager = PlayerManager(self.window.size, DIST_FROM_BASE, self.textures['plane'], SPEED)

        self.obstacles = list(self.create_obstacles())
        self.stopped = False
        self.gameover = create_sprite(self.textures['aliens_win'], self.window.width, self.window.height, (0, 0))


    def run(self):
        while self.window.is_open:
            for event in self.window.events:
                self.handle_events(event)

            elapsed = self.clock.elapsed_time.seconds
            self.clock.restart()
            self.update(elapsed)

            self.render()

    def handle_events(self, event):
        if type(event) is sf.CloseEvent:
            self.window.close()
        else:
            self.player_manager.handle_event(event, self.collision_manager)

    def update(self, elapsed_time):
        for obstacle in self.obstacles:
            obstacle.update(self.window.size.y, elapsed_time)

        self.player_manager.update(elapsed_time)
        self.collision_manager.update()
        self.check_for_game_end()

    def render(self):
        self.window.clear()

        self.window.draw(self.bg)
        if not self.stopped:
            self.player_manager.render(self.window)
            for obstacle in self.obstacles:
                obstacle.render(self.window)
            for base in self.bases:
                base.render(self.window)
        else:
            self.window.draw(self.gameover)

        self.window.display()

    def update_obstacles(self, elapsed_time):
        for obstacle in self.obstacles:
            obstacle.update(self.window.size.y, elapsed_time)

    def check_for_game_end(self):
        if self.bases[0].lives == 0:
            self.stopped = True
            self.gameover = create_sprite(self.textures['aliens_win'] if self.bases[0].id == 'left' else self.textures['humans_win'], self.window.width, self.window.height, (0, 0))
        if self.bases[1].lives == 0:
            self.stopped = True
            self.gameover = create_sprite(self.textures['humans_win'] if self.bases[0].id == 'left' else self.textures['aliens_win'], self.window.width, self.window.height, (0, 0))


    @staticmethod
    def load_assets():
        try:
            return {
                'bg': sf.Texture.from_file("assets/images/background.png"),
                'obstacle': sf.Texture.from_file("assets/images/obstacle.png"),
                'red': sf.Texture.from_file("assets/images/red03.png"),
                'green': sf.Texture.from_file("assets/images/green03.png"),
                'plane': sf.Texture.from_file("assets/images/plane_sheet.png"),
                'aliens_win': sf.Texture.from_file("assets/images/aliens_win.png"),
                'humans_win': sf.Texture.from_file("assets/images/humans_win.png")
            }
        except IOError:
            sys.exit(1)

    def create_obstacles(self):
        for i in xrange(1, NUMBER_OF_OBSTACLES + 1):
            x_pos = DIST_FROM_BASE + (WWIDTH * 1.0 - 2 * DIST_FROM_BASE) * i / (NUMBER_OF_OBSTACLES + 1)
            print x_pos
            obstacle = ObstacleLine(200, 50, x_pos, texture=self.textures['obstacle'])
            self.collision_manager.add(obstacle)
            yield obstacle

    def create_bases(self):
        bases = [Base("left", LIVES, self.textures['red'], self.textures['green'], self.window.height, self.window.width),
                Base("right", LIVES, self.textures['red'], self.textures['green'], self.window.height, self.window.width)]

        for base in bases:
            self.collision_manager.add(base)

        return bases


if __name__ == '__main__':
    Game().run()