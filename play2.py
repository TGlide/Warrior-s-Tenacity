# -*- coding: utf-8 -*-

from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from time import sleep, time
from os import getcwd, sep
from random import choice, randint
from helpers import *


def play(wn, dif):
    ###########
    # Classes #
    ###########
    class Ein:
        def __init__(self):
            # Dicionário com spritesheets para diferentes estados
            self.sprites = {
                'idle': Sprite(get_sprite("ein{}idle.png".format(sep)), 4),
                'attack1': Sprite(get_sprite("ein{}attack1.png".format(sep)), 5),
                'attack2': Sprite(get_sprite("ein{}attack2.png".format(sep)), 6),
                'walk': Sprite(get_sprite("ein{}walk.png".format(sep)), 6),
                'jump': Sprite(get_sprite("ein{}jump.png".format(sep)), 10),
            }
            # Setar duração da animação dos sprite sheets
            for s in self.sprites.values():
                s.set_total_duration(500)

            self.current = 'idle'  # Estado atual
            self.direction = "R"

            self.x = wn.width/2 - self.sprites[self.current].width/2
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = 3
            self.life_sprites = [Sprite(get_sprite("ein{}life.png".format(
                sep)), 2,  size=(82, 41)) for i in range(self.life)]
            life_x_init = wn.width/2 - (self.life_sprites[0].width/2)*self.life
            for s in self.life_sprites:
                s.set_total_duration(1)
                s.set_position(life_x_init, self.y + self.height + 30)
                life_x_init += self.life_sprites[0].width
            self.hit_timer = time()

            self.reach = 70  # Alcance de Ein ate os inimigos

            self.rs_l = Sprite(get_sprite("reach.png"), 1, size=(32, 60))
            self.rs_l.set_position(
                self.x - self.reach - self.rs_l.width, self.y+self.height-self.rs_l.height/2)
            self.rs_r = Sprite(get_sprite("reach.png"), 1, size=(32, 60))
            self.rs_r.set_position(
                self.x + self.width + self.reach, self.y+self.height-self.rs_r.height/2)

            self.attack_pool = 0  # Conta quantos ataques foram efetuados
            self.attack_timer = time()

            self.speed = 80
            self.walking = False
            self.attacking = False

            self.jumpspeed = 1200
            self.jumpaux = self.jumpspeed
            self.gravity = 2700

        def jump(self):
            self.y += -self.jumpaux*wn.delta_time()
            self.jumpaux -= self.gravity*wn.delta_time()
            if self.current != "jump":
                self.change_sprite("jump")
                self.sprites[self.current].set_curr_frame(0)
                self.sprites[self.current].play()

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def powerup(self, power):
            if power == "life":
                self.life += 2
                self.life_sprites.append(
                    Sprite(get_sprite("ein{}life.png".format(sep)), 2,  size=(82, 41)))
                self.take_hit()
                life_x_init = wn.width/2 - \
                    (self.life_sprites[0].width/2)*len(self.life_sprites)
                for s in self.life_sprites:
                    s.set_total_duration(1)
                    s.set_position(life_x_init, self.y + self.height + 30)
                    life_x_init += self.life_sprites[0].width

            elif power == "reach":
                self.reach += 10
                self.rs_l.set_position(
                    self.x - self.reach - self.rs_l.width, self.y+self.height-self.rs_l.height/2)
                self.rs_r.set_position(
                    self.x + self.width + self.reach, self.y+self.height-self.rs_r.height/2)

        def change_sprite(self, sprite):
            self.current = sprite if self.current != sprite else self.current

        def action(self, kb, monsters):
            # Jumping
            if self.jumpspeed != self.jumpaux:
                self.jump()
            if self.jumpspeed == self.jumpaux and kb.key_pressed("UP"):
                self.jumpaux -= 1
                return
            if self.jumpaux < -self.jumpspeed:
                self.jumpaux = self.jumpspeed
                self.y = wn.height - 122 - self.sprites[self.current].height
                self.change_sprite('idle')

            # Turning directions
            if kb.key_pressed("left"):
                self.direction = "L"
                if self.current != "jump":
                    self.change_sprite("idle")
            elif kb.key_pressed("right"):
                self.direction = "R"
                if self.current != "jump":
                    self.change_sprite("idle")
            # Attacking
            else:
                if time() - self.attack_timer >= 1/self.cps:
                    if self.direction == "R":
                        monsters = list(sorted(filter(lambda m: m.next_key(
                        ) and m.sprites[m.current].x + m.sprites[m.current].width/2 > wn.width/2, monsters), key=lambda mon: mon.x)) # Monsters to the right
                        for m in monsters:
                            if wn.width/2 <= m.x <= self.x+self.width + self.reach and m.next_key() and kb.key_pressed(m.next_key().key):
                                self.attack_timer = time()
                                m.next_key().press()
                                self.attack(m)
                                attack_sfx.play()

                    else:
                        monsters = list(sorted(filter(lambda m: m.next_key(
                        ) and m.sprites[m.current].x + m.sprites[m.current].width/2 < wn.width/2, monsters), key=lambda mon: -mon.x))
                        for m in monsters:
                            if self.x - self.reach <= m.x + m.width <= wn.width/2 and m.next_key() and kb.key_pressed(m.next_key().key):
                                self.attack_timer = time()
                                m.next_key().press()
                                self.attack(m)
                                attack_sfx.play()

        def attack(self, m):
            if "attack" not in self.current:
                self.change_sprite("attack1")
                self.sprites[self.current].set_curr_frame(0)
                self.sprites[self.current].play()
            else:
                self.attack_pool += 1

        def take_hit(self):
            if self.life > 0:
                self.life -= 1
                for i in range(len(self.life_sprites)):
                    self.life_sprites[i].set_curr_frame(
                        0 if i < self.life else 1)
            else:
                self.life = len(self.life_sprites)
                for s in self.life_sprites:
                    s.update()

        def update(self):
            # if self.current == "walk":
            #     if self.dest.x > self.x + self.width + 10:
            #         self.x += self.speed * wn.delta_time()
            #     else:
            #         self.x = self.dest.x - self.width - 10
            #         self.attack(self.dest)

            if "attack" in self.current:  # Se estiver atacando
                # Acabou uma animação de ataque
                if self.attack_pool > 0:
                    self.attack_pool -= 1
                    next_attack = int(self.current[-1]) % 2 + 1
                    self.change_sprite("attack" + str(next_attack))
                    self.sprites[self.current].set_curr_frame(0)
                    self.sprites[self.current].play()

                elif not self.sprites[self.current].is_playing():
                    self.change_sprite("idle")

            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw(flip=self.direction == "L")
            for l in self.life_sprites:
                l.draw()
            self.rs_l.draw(flip=True)
            self.rs_r.draw()

    class Key:
        keys = "asdf"

        def __init__(self, k=None):
            if not k:
                k = choice(self.keys)
            self.sprite = Sprite(
                get_sprite("keys{}{}.png".format(sep, k)), frames=2, size=(48, 23))
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
            self.sprites = {
                'idle': Sprite(get_asset("skelly{}idle.png".format(sep)), 11, size=(100,125)),
                'attack': Sprite(get_asset("skelly{}attack.png".format(sep)), 18),
                'walk': Sprite(get_asset("skelly{}walk.png".format(sep)), 13, size=(100,125)),
                'dead': Sprite(get_asset("skelly{}dead.png".format(sep)), 15, size=(150,125))
            }
            # Setar duração da animação dos sprite sheets
            for s in self.sprites.values():
                s.set_total_duration(750)

            self.current = 'walk'  # Estado atual

            self.attacked = False  # Auxiliar para impedir multiplos ataques a Ein

            self.direction = direction
            self.x = [-self.sprites[self.current].width,
                      wn.width][direction == "R"] if not x else x
            self.y = wn.height - 122 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.dead = False
            # self.reach = 50
            self.speed = 200

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def change_sprite(self, sprite):
            if self.current != sprite:
                self.current = sprite
                self.sprites[self.current].set_curr_frame(0)
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
                    if m.x <= self.x - 10 <= m.x + m.width :
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
            
        def death(self):
            self.change_sprite("dead")
            
            if self.sprites[self.current].get_curr_frame() == self.sprites[self.current].get_final_frame() - 1:
                self.dead = True
            

        def update(self):
            self.sprites[self.current].set_position(self.x, self.y)
            self.sprites[self.current].update()

        def draw(self):
            self.sprites[self.current].draw(flip=[False, True][self.direction=="L"])

    #############
    # Variables #
    #############
    DEBUGGING = True

    background = GameImage(get_asset("bg.png"), (wn.width, wn.height))
    ein = Ein()

    monsters = [Skelly(life=2), Skelly(life=1, direction="R")]

    timer = time()
    mouse = wn.get_mouse()
    mt = time()

    #############
    # Game Loop #
    #############
    while True:
        background.draw()

        ein.update()
        ein.draw()

        mouse_over_monster = False

        # Update os monstros
        for m in monsters[:]:
            # Para debuggar
            if mouse.is_over_object(m) and DEBUGGING:
                mouse_over_monster = True
                if mouse.is_button_pressed(1) and time() - mt > 0.5:
                    mt = time()
                    m.life = 0
                    continue
            # Fim debug
            m.define_action([i for i in monsters if i != m], ein)
            m.update()
            m.draw()
            if m.dead:
                monsters.remove(m)
                killed_monsters += 1
        
        # Para debuggar
        if mouse.is_button_pressed(1) and not mouse_over_monster and time() - mt > 0.5 and DEBUGGING:
            mt = time()
            mx = mouse.get_position()[0]
            monsters.append(Skelly(life=1, direction = ["R", "L"][mx >= wn.width/2], x=mx))
        # Fim debug

        wn.update()


    if __name__ == "__main__":
        play(Window(1366, 768),1)