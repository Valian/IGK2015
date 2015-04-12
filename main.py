#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf
import sys
from player import PlayerManager
from utils import *
from animation import *
from obstacle import ObstacleLine

WWIDTH, WHEIGHT = 1200, 750
WTITLE = "IGK 2015"
DIST_FROM_BASE = 100
SPEED = 200

SETTINGS = sf.ContextSettings()
SETTINGS.antialiasing_level = 8


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
        self.bg = create_sprite(self.textures['bg'], WWIDTH, WHEIGHT)

        self.player_manager = PlayerManager(self.window.size, DIST_FROM_BASE, self.textures['plane'], SPEED)

        self.obstacles = self.create_obstacles()

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
            self.player_manager.handle_event(event)

    def update(self, elapsed_time):
        for obstacle in self.obstacles:
            obstacle.update(self.window.size.y, elapsed_time)

        self.player_manager.update(elapsed_time)

    def render(self):
        self.window.clear()

        self.window.draw(self.bg)
        self.player_manager.render(self.window)
        for obstacle in self.obstacles:
            obstacle.render(self.window)

        self.window.display()

    @staticmethod
    def load_assets():
        try:
            return {
                'bg': sf.Texture.from_file("assets/images/background.png"),
                'obstacle': sf.Texture.from_file("assets/images/rock-up.png"),
                'plane': sf.Texture.from_file("assets/images/plane_sheet.png")
            }
        except IOError:
            sys.exit(1)

    def create_obstacles(self):
        obstacles = [ObstacleLine(10, 100, 200, texture=self.textures['obstacle'])]
        return obstacles


if __name__ == '__main__':
    Game().run()