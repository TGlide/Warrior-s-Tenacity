from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from time import sleep, time
from os import getcwd, sep
from random import choice
from helpers import *


def play(wn, dif):
    class Ein:
        def __init__(self):
            self.sprites = {
                'idle': Sprite(get_asset("ein{}idle.png".format(sep)), 4),
                'attack': Sprite(get_asset("ein{}attack.png".format(sep)), 7),
                'walk': Sprite(get_asset("ein{}walk.png".format(sep)), 6),
            }
            for s in self.sprites.values():
                s.set_total_duration(500)

            self.current = 'idle'

            self.x = wn.width/2 - self.sprites[self.current].width/2
            self.y = wn.height - 122 - self.sprites[self.current].height
            self.life = 6
            self.reach = 50

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw()

    class Skelly:
        def __init__(self, life, direction="L"):
            self.sprites = {
                'idle': Sprite(get_asset("skelly{}idle.png".format(sep)), 11),
                'attack': Sprite(get_asset("skelly{}attack.png".format(sep)), 18),
                'walk': Sprite(get_asset("skelly{}walk.png".format(sep)), 13),
            }
            for s in self.sprites.values():
                s.set_total_duration(500)

            self.current = 'walk'

            self.direction = direction
            self.x = [0, wn.width][direction == "L"]
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.reach = 50
            self.speed = 500

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def change_sprite(self, sprite):
            self.current = sprite
            self.sprites[self.current].set_curr_frame = 0

        def define_action(self, monsters, ein):
            if self.direction == "L":
                if ein.x + ein.width < self.x < ein.x+ein.width+ein.reach:
                    self.set_pos(ein.x + ein.width + ein.reach, self.y)
                    self.idle()
                    return
            for m in monsters:
                if self.direction == "L":
                    if m.x <= self.x <= m.x + m.width:
                        self.set_pos(m.x + m.width + 10, self.y)
                        self.idle()
                        return
            self.move()

        def idle(self):
            self.change_sprite("idle")

        def move(self):


        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw()

    #############
    # Variables #
    #############
    background = GameImage(get_asset("bg.png"), (wn.width, wn.height))
    ein = Ein()
    while True:
        background.draw()

        ein.update()
        ein.draw()

        wn.update()


if __name__ == "__main__":
    play(Window(1366, 768), 1)
