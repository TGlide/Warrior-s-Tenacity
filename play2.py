# -*- coding: utf-8 -*-

from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from PPlay.font import *
from time import sleep, time
from os import getcwd, sep
from random import choice
from helpers import *


def play(wn, dif):
    ###########
    # Classes #
    ###########
    class Ein:
        def __init__(self):
            # Dicionário com spritesheets para diferentes estados
            self.sprites = {
                'idle': Sprite(get_asset("ein{}idle.png".format(sep)), 4),
                'attack1': Sprite(get_asset("ein{}attack1.png".format(sep)), 5),
                'attack2': Sprite(get_asset("ein{}attack2.png".format(sep)), 6),
                'walk': Sprite(get_asset("ein{}walk.png".format(sep)), 6),
            }
            # Setar duração da animação dos sprite sheets
            for i in range(1, 3):
                self.sprites['attack' + str(i)].set_loop(False)
                self.sprites['attack' + str(i)].set_total_duration(325)
            for s in self.sprites.values():
                s.set_total_duration(500)

            self.current = 'idle'  # Estado atual
            self.direction = "R"

            self.x = wn.width/2 - self.sprites[self.current].width/2
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = 6
            self.reach = 50  # Alcance de Ein ate os inimigos

            self.rs_l = Sprite(get_asset("reach.png"), 1, size=(32, 60))
            self.rs_l.set_position(
                self.x - self.reach - self.rs_l.width, self.y+self.height-self.rs_l.height/2)
            self.rs_r = Sprite(get_asset("reach.png"), 1, size=(32, 60))
            self.rs_r.set_position(
                self.x + self.width + self.reach, self.y+self.height-self.rs_r.height/2)

            self.action_timer = time()
            self.attack_pool = 0  # Conta quantos ataques foram efetuados

            self.speed = 80
            self.walking = False
            self.attacking = False

            self.jumpspeed = 1000
            self.jumpaux = self.jumpspeed
            self.gravity = 2000

        def jump(self):
            self.y += -self.jumpaux*wn.delta_time()
            self.jumpaux -= self.gravity*wn.delta_time()

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def change_sprite(self, sprite):
            self.current = sprite if self.current != sprite else self.current

        def action(self, kb, monsters):
            if self.jumpspeed != self.jumpaux:
                self.jump()
            if self.jumpspeed == self.jumpaux and kb.key_pressed("UP"):
                self.jumpaux -= 1
                return
            if self.jumpaux < -self.jumpspeed:
                self.jumpaux = self.jumpspeed
                self.y = wn.height - 122 - self.sprites[self.current].height
            if self.attacking:  # TODO
                return
            if kb.key_pressed("left"):
                self.direction = "L"
            elif kb.key_pressed("right"):
                self.direction = "R"
            else:
                for m in monsters:
                    if m.direction == self.direction:
                        if self.direction == "R":
                            if wn.width/2 <= m.x <= self.x + self.width + self.reach:
                                if m.next_key() and kb.key_pressed(m.next_key().key):
                                    m.next_key().press()
                                    self.attack(m)
                        else:
                            if self.x - self.reach <= m.x + m.width <= self.x:
                                if m.next_key() and kb.key_pressed(m.next_key().key):
                                    m.next_key().press()
                                    self.attack(m)

        def attack(self, m):
            # if self.direction == "R":
            #     if m.x > self.x + self.width + 10:
            #         print("fuck")
            #         self.change_sprite("walk")
            #         self.dest = m
            #         return
            if "attack" not in self.current:
                self.change_sprite("attack1")
                self.sprites[self.current].set_curr_frame(0)
                self.sprites[self.current].play()
            self.attack_pool += 1

        def update(self):
            # if self.current == "walk":
            #     if self.dest.x > self.x + self.width + 10:
            #         self.x += self.speed * wn.delta_time()
            #     else:
            #         self.x = self.dest.x - self.width - 10
            #         self.attack(self.dest)

            if "attack" in self.current:  # Se estiver atacando
                # Acabou uma animação de ataque
                if not self.sprites[self.current].is_playing():
                    self.attack_pool -= 1
                    if self.attack_pool == 0:
                        self.attacking = False
                        self.change_sprite("idle")
                    else:
                        next_attack = int(self.current[-1]) % 2 + 1
                        self.change_sprite("attack" + str(next_attack))
                        self.sprites[self.current].set_curr_frame(0)
                        self.sprites[self.current].play()

            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw(flip=self.direction == "L")
            self.rs_l.draw(flip=True)
            self.rs_r.draw()

    class Key:
        keys = "zxas"

        def __init__(self, k=None):
            if not k:
                k = choice(self.keys)
            self.sprite = Sprite(
                get_asset("keys{}{}.png".format(sep, k)), frames=2, size=(48, 23))
            self.sprite.set_total_duration(100)
            self.key = k
            self.pressed = False

        def draw(self):
            self.sprite.draw()

        def set_position(self, x, y):
            self.sprite.set_position(x, y)

        def press(self):
            self.sprite.update()
            self.pressed = True

    class Skelly:
        def __init__(self, life, direction="L", x=None):
            # Dicionário com spritesheets para diferentes estados
            mf = 3.5
            self.sprites = {
                'idle': Sprite(get_asset("skelly{}idle.png".format(sep)), 11, size=(int(264*mf), int(32*mf))),
                'attack': Sprite(get_asset("skelly{}attack.png".format(sep)), 18),
                'walk': Sprite(get_asset("skelly{}walk.png".format(sep)), 13, size=(int(286*mf), int(33*mf))),
                'dead': Sprite(get_asset("skelly{}dead.png".format(sep)), 15, size=(int(495*mf), int(32*mf))),
                'hit': Sprite(get_asset("skelly{}hit.png".format(sep)), 8, size=(int(495*mf), int(32*mf))),
            }
            # Setar duração da animação dos sprite sheets
            for s in self.sprites.values():
                s.set_total_duration(800)

            self.current = 'walk'  # Estado atual

            self.direction = direction
            self.x = [-self.sprites[self.current].width,
                      wn.width][direction == "R"] if not x else x
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.keys = [Key() for i in range(life)]

            self.dead = False
            # self.reach = 50
            self.speed = 160

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
            """
            Essa função define a ação a ser tomada definida pelo contexto atual, por
            isso passamos monsters e Ein
            """
            if self.life == 0:
                self.death()
                return
            if self.direction == "R":
                if wn.width/2 <= self.x <= ein.x + ein.width + ein.reach - 110:
                    self.set_pos(ein.x + ein.width + ein.reach - 110, self.y)
                    self.idle()
                    return
            else:
                if ein.x - ein.reach + 10 <= self.x + self.width <= ein.x:
                    self.set_pos(ein.x - ein.reach + 10 - self.width, self.y)
                    self.idle()
                    return
            for m in list(filter(lambda x: type(x) != Hellhound, monsters)):
                if self.direction == "R":
                    if m.x <= self.x - 20 <= m.x + m.width:
                        self.set_pos(m.x + m.width + 20, self.y)
                        self.idle()
                        return
                else:
                    if m.x <= self.x + self.width + 20 <= m.x + m.width:
                        self.set_pos(m.x - self.width - 20, self.y)
                        self.idle()
                        return
            self.move()

        def idle(self):
            self.change_sprite("idle")

        def move(self):
            self.change_sprite("walk")
            self.x += self.speed * wn.delta_time() * \
                [-1, 1][self.direction == "L"]

        def death(self):
            self.change_sprite("dead")

            if self.sprites[self.current].get_curr_frame() == self.sprites[self.current].get_final_frame() - 1:
                self.dead = True

        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

            if self.keys:
                k_width = self.keys[0].sprite.width
                k_height = self.keys[0].sprite.height
                x_init = self.x + self.width/2 - (k_width/2)*len(self.keys)
                self.life = 0
                for k in range(len(self.keys)):
                    self.keys[k].set_position(x_init, self.y - k_height - 10)
                    x_init += k_width
                    if not self.keys[k].pressed:
                        self.life += 1

        def draw(self):
            self.sprites[self.current].draw(
                flip=[False, True][self.direction == "R"])
            for k in self.keys:
                k.draw()

        def next_key(self):
            for k in self.keys:
                if not k.pressed:
                    return k
            return None

    class Hellhound:
        def __init__(self, life, direction="L", x=None):
            # Dicionário com spritesheets para diferentes estados
            self.sprites = {
                'idle': Sprite(get_asset("hellhound{}PNG{}idle.png".format(sep, sep)), 6, size=(1000, 125)),
                'walk': Sprite(get_asset("hellhound{}PNG{}walk.png".format(sep, sep)), 12, size=(1000, 125)),
                'run': Sprite(get_asset("hellhound{}PNG{}run.png".format(sep, sep)), 5, size=(1000, 125)),
                'dead': Sprite(get_asset("skelly{}dead.png".format(sep)), 15, size=(1000, 125))
            }
            # Setar duração da animação dos sprite sheets
            for s in self.sprites.values():
                s.set_total_duration(600)

            self.current = 'run'  # Estado atual

            self.direction = direction
            self.x = [-self.sprites[self.current].width,
                      wn.width][direction == "L"] if not x else x
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.dead = False
            # self.reach = 50
            self.speed = 250

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
            """
           necessario mudaças porque o hellhound ta para como esqueleto
            """
            if self.life == 0:
                self.death()
                return
            if self.x > wn.width and self.direction == "R":

                self.direction = "L"
                self.speed = self.speed
            if self.x < 0-self.width and self.direction == "L":

                self.direction = "R"
                self.speed = self.speed
            self.move()

        def idle(self):
            self.change_sprite("idle")

        def move(self):
            self.change_sprite("run")
            self.x += self.speed * wn.delta_time() * \
                [-1, 1][self.direction == "R"]

        def death(self):
            self.change_sprite("dead")

            if self.sprites[self.current].get_curr_frame() == self.sprites[self.current].get_final_frame() - 1:
                self.dead = True

        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw(
                flip=[False, True][self.direction == "R"])
        
        def next_key(self):
            return None

    #############
    # Variables #
    #############
    DEBUGGING = True

    background = GameImage(get_asset("bg.png"), (wn.width, wn.height))
    ein = Ein()
    debug_font = Font(ein.current, size=100)
    debug_font.set_position(0, 0)
    attack_pool_font = Font(str(ein.attack_pool), size=100)
    attack_pool_font.set_position(0, debug_font.height + 10)

    monsters = [Hellhound(life=2), Hellhound(life=1, direction="R")]

    timer = time()
    mouse = wn.get_mouse()
    kb = wn.get_keyboard()

    mt = time()

    #############
    # Game Loop #
    #############
    while True:
        background.draw()

        ein.action(kb, monsters)
        ein.update()
        ein.draw()

        debug_font.change_text(ein.current)
        debug_font.draw()

        attack_pool_font.change_text(str(ein.attack_pool))
        attack_pool_font.draw()

        mouse_over_monster = False

        # Update os monstros
        for m in monsters[:]:
            # Para debuggar
            if mouse.is_over_object(m) and DEBUGGING:
                mouse_over_monster = True
                if mouse.is_button_pressed(1) and time() - mt > 0.5:
                    mt = time()
                    m.life = 0
                    m.keys = []
                    continue
            # Fim debug
            m.define_action([i for i in monsters if i != m], ein)
            m.update()
            m.draw()
            if m.dead:
                monsters.remove(m)

        # Para debuggar
        if mouse.is_button_pressed(1) and not mouse_over_monster and time() - mt > 0.5 and DEBUGGING:
            mt = time()
            mx = mouse.get_position()[0]
            monsters.append(Hellhound(life=1, direction=[
                            "R", "L"][mx >= wn.width/2], x=mx))
        if mouse.is_button_pressed(3) and not mouse_over_monster and time() - mt > 0.5 and DEBUGGING:
            mt = time()
            mx = mouse.get_position()[0]
            monsters.append(
                Skelly(life=choice([1, 2, 3, 4]), direction=["L", "R"][mx >= wn.width/2], x=mx))
        # Fim debug

        wn.update()


if __name__ == "__main__":
    play(Window(1366, 768), 1)
