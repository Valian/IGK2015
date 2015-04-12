#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sfml as sf
import sys
from utils import *
from animation import *

WWIDTH, WHEIGHT = 800, 1000
WTITLE = "IGK 2015"
SETTINGS = sf.ContextSettings()
SETTINGS.antialiasing_level = 8
GRAVITY = 10.0


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

    def update(self, elapsed_time):
        pass

    def render(self):
        self.window.clear()

        self.window.draw(self.bg)
        self.window.display()

    @staticmethod
    def load_assets():
        try:
            return {
                'bg': sf.Texture.from_file("assets/images/background.png")
            }
        except IOError:
            sys.exit(1)


if __name__ == '__main__':
    Game().run()