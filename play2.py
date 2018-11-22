# -*- coding: utf-8 -*-

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

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = 6
            self.reach = 50

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw(flip=True)

    class Skelly:
        def __init__(self, life, direction="L", x=None):
            self.sprites = {
                'idle': Sprite(get_asset("skelly{}idle.png".format(sep)), 11, size=(100,125)),
                'attack': Sprite(get_asset("skelly{}attack.png".format(sep)), 18),
                'walk': Sprite(get_asset("skelly{}walk.png".format(sep)), 13, size=(100,125)),
            }
            for s in self.sprites.values():
                s.set_total_duration(800)

            self.current = 'walk'

            self.direction = direction
            self.x = [-self.sprites[self.current].width, wn.width][direction == "L"] if not x else x
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.reach = 50
            self.speed = 80

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def change_sprite(self, sprite):
            if self.current != sprite:
                self.current = sprite
                self.sprites[self.current].set_curr_frame = 0
                self.width = self.sprites[self.current].width
                self.height = self.sprites[self.current].height

        def define_action(self, monsters, ein):
            if self.direction == "L":
                if ein.x + ein.width <= self.x <= ein.x+ein.width+ein.reach:
                    self.set_pos(ein.x + ein.width + ein.reach, self.y)
                    self.idle()
                    return
            else:
                if ein.x - ein.reach <= self.x + self.width <= ein.x:
                    self.set_pos(ein.x - ein.reach - self.width, self.y)
                    self.idle()
                    return
            for m in monsters:
                if self.direction == "L":
                    if m.x <= self.x - 10 <= m.x + m.width:
                        self.set_pos(m.x + m.width + 10, self.y)
                        self.idle()
                        return
                else:
                    if m.x <= self.x + self.width + 10 <= m.x + m.width:
                        self.set_pos(m.x - self.width - 10, self.y)
                        self.idle()
                        return
            self.move()

        def idle(self):
            self.change_sprite("idle")

        def move(self):
            self.change_sprite("walk")
            self.x += self.speed * wn.delta_time() * [-1, 1][self.direction=="R"]
            

        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw(flip=[False, True][self.direction=="L"])

    #############
    # Variables #
    #############
    background = GameImage(get_asset("bg.png"), (wn.width, wn.height))
    ein = Ein()

    monsters = [Skelly(life=2), Skelly(life=1, direction="R")]
    timer = time()
    mouse = wn.get_mouse()
    mt = time()
    while True:
        background.draw()

        if time() - timer >= 3:
            monsters.append(Skelly(life=1, direction="L"))
            timer = float('inf')
        ein.update()
        ein.draw()

        mouse_over_monster = False

        for m in monsters[:]:
            if mouse.is_over_object(m):
                mouse_over_monster = True
                if mouse.is_button_pressed(1) and time() - mt > 0.5:
                    mt = time()
                    monsters.remove(m)
                    continue
            m.define_action([i for i in monsters if i != m], ein)
            m.update()
            m.draw()
        
        if mouse.is_button_pressed(1) and not mouse_over_monster and time() - mt > 0.5:
            mt = time()
            mx = mouse.get_position()[0]
            monsters.append(Skelly(life=1, direction = ["R", "L"][mx >= wn.width/2], x=mx))

        wn.update()


if __name__ == "__main__":
    play(Window(1366, 768), 1)
