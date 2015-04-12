import sfml as sf
from abc import ABCMeta, abstractmethod


class Collidable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_bounding_rect(self):
        pass

    @abstractmethod
    def collide(self, other):
        pass


class CollisionManager(object):
    def __init__(self):
        self.objects = []


