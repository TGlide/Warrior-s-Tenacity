# -*- coding: utf-8 -*-

from PPlay.window import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.sprite import *
from PPlay.sound import *
from PPlay.font import *


from time import sleep, time
from os import getcwd, sep
from random import choice, randint
from helpers import *


def play(wn, dif):
    ###########
    # Classes #
    ###########
    class Attribute:
        mf = 3

        def __init__(self, attr, total):
            self.icon = Sprite(get_sprite("attribute{}{}.png".format(
                os.sep, attr)), size=(16*self.mf, 16*self.mf))
            self.levels = [Sprite(get_sprite("attribute{}{}_level.png".format(
                os.sep, attr)), size=(32*self.mf, 16*self.mf), frames=2) for i in range(total)]
            for l in self.levels:
                l.set_total_duration(1)
            
            self.level = 0
            self.total = total

        def set_position(self, x, y):
            self.icon.set_position(x, y)
            for i in range(len(self.levels)):
                self.levels[i].set_position(
                    self.icon.x + self.icon.width + (self.levels[0].width)*i, y)

        def add(self):
            self.levels[self.level].update()
            self.level += 1

        def draw(self):
            self.icon.draw()
            for l in self.levels:
                l.draw()

    class Item:
        mf = 1.5

        def __init__(self, itm):
            self.icon = Sprite(get_sprite("item{}{}.png".format(
                os.sep, itm)), size=(int(96*self.mf), int(48*self.mf)), frames=2)
            self.icon.set_total_duration(1)

            self.qtd = 1
            self.qtd_font = Font("x" + str(self.qtd), font_family=font_path(
                "BitPotionExt"), color=(255, 255, 255), size=50, local_font=True)
            self.icon.set_curr_frame(0 if self.qtd == 0 else 1)

            self.use_timer = time()

        def set_position(self, x, y):
            self.icon.set_position(x, y)
            self.qtd_font.set_position(self.icon.x + self.icon.width - self.qtd_font.width,
                                       self.icon.y + self.icon.height - self.qtd_font.height)

        def add(self):
            self.qtd += 1
            if self.qtd == 1:
                self.icon.set_curr_frame(1)
            self.qtd_font.change_text("x" + str(self.qtd))
            self.qtd_font.set_position(self.icon.x + self.icon.width - self.qtd_font.width,
                                       self.icon.y + self.icon.height - self.qtd_font.height)

        def use(self):
            self.qtd -= 1
            if self.qtd == 0:
                self.icon.set_curr_frame(0)
            self.use_timer = time()
            self.qtd_font.change_text("x" + str(self.qtd))
            self.qtd_font.set_position(self.icon.x + self.icon.width - self.qtd_font.width,
                                       self.icon.y + self.icon.height - self.qtd_font.height)

        def draw(self):
            self.icon.draw()
            if self.qtd != 0:
                self.qtd_font.draw()

    class Ein:
        cps = 10  # Characters per second permitted

        def __init__(self):
            # Dicionário com spritesheets para diferentes estados
            self.sprites = {
                'idle': Sprite(get_sprite("ein{}idle.png".format(sep)), 4),
                'attack1': Sprite(get_sprite("ein{}attack1.png".format(sep)), 5),
                'attack2': Sprite(get_sprite("ein{}attack2.png".format(sep)), 6),
                'attackjump': Sprite(get_sprite("ein{}attackjump.png".format(sep)), 4),
                'walk': Sprite(get_sprite("ein{}walk.png".format(sep)), 6),
                'jump': Sprite(get_sprite("ein{}jump.png".format(sep)), 10),
                'death': Sprite(get_sprite("ein{}death.png".format(sep)), 7)
            }
            # Setar duração da animação dos sprite sheets
            self.sprites['jump'].set_loop(False)
            self.sprites['attackjump'].set_loop(False)
            self.sprites['attackjump'].set_total_duration(325)
            self.sprites['death'].set_loop(False)
            for i in range(1, 3):
                self.sprites['attack' + str(i)].set_loop(False)
                self.sprites['attack' + str(i)].set_total_duration(325)
            for s in self.sprites.values():
                s.set_total_duration(500)

            self.current = 'idle'  # Estado atual
            self.direction = "R"

            self.x = wn.width/2 - self.sprites[self.current].width/2
            self.y = wn.height - 100 - self.sprites[self.current].height

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
            self.jumptimer = time() # Impede spam de pulo

        def jump(self):
            self.y += -self.jumpaux*wn.delta_time()
            self.jumpaux -= self.gravity*wn.delta_time()
            if self.current != "jump" and (self.current != "attackjump" or (self.current == "attackjump" and not self.sprites[self.current].is_playing())) and self.current != "death":
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

        def action(self, kb, monsters, bloody, potion):
            # DEATH
            if self.life == 0:
                self.change_sprite("death")
                
            # Jumping
            if self.jumpspeed != self.jumpaux:
                self.jump()
            if self.jumpspeed == self.jumpaux and kb.key_pressed("UP") and time() - self.jumptimer > 0.36:
                self.jumpaux -= 1
                return
            if self.jumpaux < -self.jumpspeed:
                self.jumpaux = self.jumpspeed
                self.y = wn.height - 100 - self.sprites[self.current].height
                self.change_sprite('idle' if self.current != "death" else "death")
                self.jumptimer = time()

            # Turning directions
            if kb.key_pressed("left"):
                self.direction = "L"
                if self.current != "jump":
                    self.change_sprite("idle")
            elif kb.key_pressed("right"):
                self.direction = "R"
                if self.current != "jump":
                    self.change_sprite("idle")
            # Potion
            elif kb.key_pressed("q"):
                if potion.qtd > 0 and self.life < len(self.life_sprites) and time() - potion.use_timer > 1:
                    potion.use()
            
                    self.life += 2
                    self.take_hit()
            # Sanguinário
            elif kb.key_pressed("e"):
                if bloody.qtd > 0 and time() - bloody.use_timer > 1:
                    bloody.use()
                    for m in monsters:
                        for k in list(filter(lambda x: not x.pressed, m.keys)):
                            k.press()
                        m.life=0
            # Attacking
            else:
                if time() - self.attack_timer >= 1/self.cps:
                    if self.direction == "R":
                        monsters = list(sorted(filter(lambda m: m.next_key(
                        ) and m.sprites[m.current].x + m.sprites[m.current].width/2 > wn.width/2, monsters), key=lambda mon: mon.x))  # Monsters to the right
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
                if self.current == "jump":
                    self.change_sprite("attackjump")
                else:
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
                    if self.current != "attackjump":
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
        mf = 3.5

        def __init__(self, life, direction="L", x=None):
            # Dicionário com spritesheets para diferentes estados

            self.sprites = {
                'idle': Sprite(get_sprite("skelly{}idle.png".format(sep)), 11, size=(int(264*self.mf), int(32*self.mf))),
                'attack': Sprite(get_sprite("skelly{}attack.png".format(sep)), 18, size=(int(774*self.mf), int(37*self.mf))),
                'walk': Sprite(get_sprite("skelly{}walk.png".format(sep)), 13, size=(int(286*self.mf), int(33*self.mf))),
                'dead': Sprite(get_sprite("skelly{}dead.png".format(sep)), 15, size=(int(495*self.mf), int(32*self.mf))),
                'hit': Sprite(get_sprite("skelly{}hit.png".format(sep)), 8, size=(int(495*self.mf), int(32*self.mf))),
            }
            # Setar duração da animação dos sprite sheets
            self.sprites['attack'].set_total_duration(1500)
            for s in self.sprites.values():
                s.set_total_duration(750)

            self.current = 'walk'  # Estado atual

            self.attacked = False  # Auxiliar para impedir multiplos ataques a Ein

            self.direction = direction
            self.x = [-self.sprites[self.current].width,
                      wn.width][direction == "R"] if not x else x
            self.y = wn.height - 100 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.pts = life*10
            self.keys = []
            last_key = None
            for i in range(life):
                key = choice(list(filter(lambda k: k != last_key, Key.keys)))
                last_key = key
                self.keys.append(Key(k=key))

            self.dead = False
            # self.reach = 50
            self.speed = 200

        def set_pos(self, x, y):
            self.x = x
            self.y = y

        def change_sprite(self, sprite):
            if self.current != sprite:
                if self.current == "attack":  # Remove attack offset
                    self.y += 5*self.mf
                self.current = sprite
                self.sprites[self.current].set_curr_frame(0)
                self.width = self.sprites[self.current].width
                self.height = self.sprites[self.current].height
                if self.current == "attack":  # Add attack offset
                    self.y -= 5*self.mf

        def define_action(self, monsters, ein):
            """
            Essa função define a ação a ser tomada definida pelo contexto atual, por
            isso passamos monsters e Ein
            """
            if self.life == 0:
                self.death()
                return
            if self.current != "attack":
                if self.direction == "R":
                    if self.x <= ein.x + ein.width - 20:
                        self.set_pos(ein.x + ein.width - 70, self.y)
                        self.attack(ein)
                        return
                else:
                    if self.x + self.width >= ein.x - 5:
                        self.set_pos(ein.x - 10 - self.width, self.y)
                        self.attack(ein)
                        return

                for m in list(filter(lambda x: type(x) != Hellhound and x.next_key() and x != self, monsters)):
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
            else:
                if self.sprites[self.current].curr_frame == 0:
                    self.attacked = False
                if 7 <= self.sprites[self.current].curr_frame <= 9 and self.sprites[self.current].collided(ein.sprites[ein.current]) and not self.attacked:
                    ein.take_hit()
                    self.attacked = True

        def idle(self):
            self.change_sprite("idle")

        def move(self):
            self.change_sprite("walk")
            self.x += self.speed * wn.delta_time() * \
                [-1, 1][self.direction == "L"]

        def attack(self, ein):
            self.change_sprite("attack")

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
        mf = 2.5

        def __init__(self, life, direction="L", x=None):
            # Dicionário com spritesheets para diferentes estados
            self.sprites = {
                'idle': Sprite(get_sprite("hellhound{}PNG{}idle.png".format(sep, sep)), 6, size=(1000, 125)),
                'walk': Sprite(get_sprite("hellhound{}PNG{}walk.png".format(sep, sep)), 12, size=(1000, 125)),
                'run': Sprite(get_sprite("hellhound{}PNG{}run.png".format(sep, sep)), 5, size=(int(225*self.mf), int(32*self.mf))),
                'dead': Sprite(get_sprite("hellhound{}PNG{}death.png".format(sep, sep)), 7, size=(360,48))
            }
            # Setar duração da animação dos sprite sheets
            for s in self.sprites.values():
                s.set_total_duration(600)

            self.current = 'run'  # Estado atual

            self.attacked = False  # Auxiliar para impedir multiplos ataques a Ein
            self.coll_obj = GameObject()  # Auxiliar para detectar colisão com Ein
            self.coll_obj.x = wn.width/2 - 5
            self.coll_obj.width = 10

            self.direction = direction
            self.x = [-self.sprites[self.current].width,
                      wn.width][direction == "R"] if not x else x
            self.y = wn.height - 100 - self.sprites[self.current].height

            self.width = self.sprites[self.current].width
            self.height = self.sprites[self.current].height

            self.life = life
            self.pts = life*5
            self.keys = []
            last_key = None
            for i in range(life):
                key = choice(list(filter(lambda k: k != last_key, Key.keys)))
                last_key = key
                self.keys.append(Key(k=key))

            self.dead = False
            # self.reach = 50
            self.speed = 300

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

            self.coll_obj.y = ein.y
            self.coll_obj.height = ein.height

            if self.sprites[self.current].collided(self.coll_obj) and not self.attacked:
                ein.take_hit()
                self.attacked = True

            if self.x > wn.width and self.direction == "L":
                self.attacked = False
                self.direction = "R"
                self.speed = self.speed
            elif self.x < 0-self.width and self.direction == "R":
                self.attacked = False
                self.direction = "L"
                self.speed = self.speed

            self.move()

        def idle(self):
            self.change_sprite("idle")

        def move(self):
            self.change_sprite("run")
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
                flip=[False, True][self.direction == "L"])
            for k in self.keys:
                k.draw()

        def next_key(self):
            for k in self.keys:
                if not k.pressed:
                    return k
            return None

    class Score(Font):
        def __init__(self):
            Font.__init__(self, "SCORE: 0", font_family=font_path(
                "MatchupPro"), size=42, color=(255, 255, 255), local_font=True)
            self.set_position(wn.width/2 - self.width/2, 35)
            self.score = 0

        def add(self, pts):
            self.score += pts
            self.change_text("SCORE: " + str(self.score))
            self.set_position(wn.width/2 - self.width/2, self.y)

    #############
    # Variables #
    #############
    DEBUGGING = False

    # Game Objects
    background = GameImage(get_asset("bg.png"), (wn.width, wn.height))
    ein = Ein()
    monsters = []

    # Sounds #
    bg_music = Sound(get_asset("danse.wav"))
    bg_music.set_repeat(True)
    attack_sfx = Sound(get_sfx("sword_hit.ogg"))
    attack_sfx.increase_volume(90)

    # Fonts #
    # fps_font = Font("FPS: 0", size=42, color=(255, 255, 255))
    # fps_font.set_position(wn.width - fps_font.width, 0)
    # fps_timer = time()
    # frame_count = 0

    # Wave Info
    wave_count = Font("WAVE 1", size=60, font_family=font_path(
        "ExpressionPro"), local_font=True, color=(255, 255, 255))
    wave_count.set_position(wn.width/2 - wave_count.width/2, 5)

    # killed_font = Font("KILLED ON WAVE: 0/0", size=30, font_family=font_path("ExpressionPro"), local_font=True, color=(255,255,255))
    # killed_font.set_position(0, 0)
    # monsters_font = Font("ALIVE: 0", size=30, font_family=font_path("ExpressionPro"), local_font=True, color=(255,255,255))
    # monsters_font.set_position(0, killed_font.y + killed_font.height + 10)

    wave = 1
    wave_loop = True  # Auxiliar

    wave_font = Font("Wave %d" % wave, font_family=font_path(
        "arcadeclassic"), size=100, color=(0, 0, 0), local_font=True)
    wave_font.set_position(wn.width/2 - wave_font.width/2,
                           wn.height/2 - wave_font.height/2)

    wave_timer = time()

    wave_power = False  # Auxiliar em waves que te dão atributos
    health_statup = Font("Health up", color=(
        255, 231, 46), size=69, font_family=font_path("EquipmentPro"), local_font=True)
    health_statup.set_position(
        wn.width/4 - health_statup.width/2, wave_font.y + wave_font.height + 20)
    reach_statup = Font("Reach up", color=(255, 231, 46), size=69,
                        font_family=font_path("EquipmentPro"), local_font=True)
    reach_statup.set_position(
        3*wn.width/4 - reach_statup.width/2, wave_font.y + wave_font.height + 20)

    wave_item = False
    potion_up = Font("Potion", color=(
        255, 231, 46), size=69, font_family=font_path("EquipmentPro"), local_font=True)
    potion_up.set_position(
        wn.width/4 - potion_up.width/2, wave_font.y + wave_font.height + 20)
    bloody_up = Font("Sanguinario", color=(255, 231, 46), size=69,
                        font_family=font_path("EquipmentPro"), local_font=True)
    bloody_up.set_position(
        3*wn.width/4 - bloody_up.width/2, wave_font.y + wave_font.height + 20)

    score = Score()
    score.set_position(score.x, wave_count.y + wave_count.height + 5)

    # Attributes
    health_attr = Attribute("health", 3)
    health_attr.set_position(10, 10)
    reach_attr = Attribute("reach", 6)
    reach_attr.set_position(10, health_attr.icon.y +
                            health_attr.icon.height + 10)

    # Items
    bloody = Item("bloodsw")
    bloody_font = Font("SANGUINARIO", font_family=font_path(
        "BitPotionExt"), size=30, color=(255, 255, 255), local_font=True)

    bloody.set_position(wn.width - 10 - bloody.icon.width, 10 + bloody_font.height + 5)
    bloody_font.set_position(bloody.icon.x + bloody.icon.width/2 - bloody_font.width/2, 10)

    potion = Item("potion")
    potion_font = Font("POTION", font_family=font_path(
        "BitPotionExt"), size=30,color=(255, 255, 255), local_font=True)
    potion.set_position(bloody.icon.x - 10 - potion.icon.width, 10 + potion_font.height + 5)
    potion_font.set_position(potion.icon.x + potion.icon.width/2 - potion_font.width/2, 10)

    # Controladores
    killed_monsters = 0
    max_monsters = 5
    wave_total_monsters = 14 + wave
    min_keys = 1
    max_keys = 3

    ein_death = False

    spawn_timer = time()
    mouse = wn.get_mouse()
    kb = wn.get_keyboard()

    mt = time()

    bg_music.play()

    #############
    # Game Loop #
    #############
    while True:
        if wn.get_keyboard().key_pressed("esc"):
            bg_music.stop()
            return
        # Draw UI
        background.draw()
        
        score.draw()
        
        health_attr.draw()
        reach_attr.draw()
        
        wave_count.draw()

        bloody.draw()
        bloody_font.draw()
        potion.draw()
        potion_font.draw()

        # FPS COUNTER
        # frame_count += 1
        # if time() - fps_timer >= 1:
        #     fps_font.change_text("FPS: " + str(frame_count))
        #     frame_count = 0
        #     fps_timer = time()
        # fps_font.set_position(wn.width - fps_font.width, 0)
        # fps_font.draw()

        # Ein
        ein.action(kb, monsters, bloody, potion)
        ein.update()
        ein.draw()
        # Ein Death
        if ein.life == 0 and not ein_death:
            ein_death = True
            death_timer = time()
            wave_font.change_text("GAME OVER")
            wave_font.set_position(wn.width/2 - wave_font.width/2, wave_font.y)
            

        if ein_death:
            wave_font.draw()
            if time() - death_timer > 3:
                name = input("Digite seu nome: ")[:3].upper()
                with open("placar.txt", "r") as f:
                    scores = [line.split() for line in f.readlines()]
                    if name in [x[0] for x in scores]:
                        for n in range(len(scores)):
                            if scores[n][0] == name:
                                if int(scores[n][1]) < score.score:
                                    scores[n][1] = "0"*(4-len(str(score.score))) +  str(score.score)
                    else:
                        scores.append([name, "0"*(4-len(str(score.score))) +  str(score.score)])
                print(scores)
                with open("placar.txt", "w") as f:
                    for n in scores:
                        f.write(" ".join(n) + "\n")
                bg_music.stop()
                return

        # Wave loop
        if wave_loop:
            if not time() - wave_timer > 1.5 or wave_power or wave_item:
                wave_font.draw()

                if wave_power:
                    if health_attr.level < health_attr.total:
                        health_statup.draw()
                    if reach_attr.level < reach_attr.total:
                        reach_statup.draw()

                    if mouse.is_over_object(health_statup) and mouse.is_button_pressed(1) and time() - mt > 0.5 and health_attr.level < health_attr.total:
                        mt = time()
                        ein.powerup("life")
                        health_attr.add()
                        wave_power = False
                        wave_timer = time()
                    elif mouse.is_over_object(reach_statup) and mouse.is_button_pressed(1) and time() - mt > 0.5 and reach_attr.level < reach_attr.total:
                        mt = time()
                        ein.powerup("reach")
                        reach_attr.add()
                        wave_power = False
                        wave_timer = time()
                
                elif wave_item:
                    if potion.qtd < 3:
                        potion_up.draw()
                    if bloody.qtd < 3:
                        bloody_up.draw()
                    if mouse.is_over_object(potion_up) and mouse.is_button_pressed(1) and time() - mt > 0.5 and potion.qtd < 3:
                        mt = time()
                        potion.add()
                        wave_item = False
                        wave_timer = time()
                    elif mouse.is_over_object(bloody_up) and mouse.is_button_pressed(1) and time() - mt > 0.5 and bloody.qtd < 3:
                        mt = time()
                        bloody.add()
                        wave_item = False
                        wave_timer = time()

                wn.update()
                continue

            wave_loop = False
            killed_monsters = 0
            max_monsters = 5
            wave_total_monsters = 4 + wave
            if wave >= 10:
                min_keys = 2

        # Atualiza fontes de estado
        wave_count.change_text("WAVE %d" % wave)

        # Checa fim da wave
        if killed_monsters >= wave_total_monsters:
            wave += 1
            wave_font.change_text("Wave %d" % wave)
            wave_font.set_position(wn.width/2 - wave_font.width/2, wave_font.y)
            wave_loop = True
            wave_timer = time()
            if wave % 5 == 0 and (health_attr.level < health_attr.total or reach_attr.level < reach_attr.total):
                wave_power = True
            if wave % 3 == 0 and (potion.qtd < 3 or bloody.qtd < 3):
                wave_item = True

        # Spawn monsters
        if time() - spawn_timer > 0.2:  # Intervalo entre spawn
            spawn_timer = time()
            if len(monsters) < max_monsters and len(monsters) + killed_monsters < wave_total_monsters and randint(0, 10) > 5:
                # Escolher direção aleatória pro inimigo
                dirc = choice(["L", "R"])
                x = 0 if dirc == "L" else wn.width
                # Permitir apenas n hellhounds ao mesmo tempo
                if len([m for m in monsters if type(m) == Hellhound]) < 1:
                    monster = 'Hellhound' if randint(
                        0, 100) >= 80 else 'Skelly'
                else:
                    monster = 'Skelly'
                monsters.append(eval(monster)(life=choice(
                    list(range(min_keys, max_keys + 1))), direction=dirc, x=x))
                
                spawn_timer = time() + 0.2

        mouse_over_monster = False
        # Update os monstros
        for m in monsters[:]:
            # debug
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
                score.add(m.pts)
                monsters.remove(m)
                killed_monsters += 1

        # Para debuggar
        if mouse.is_button_pressed(1) and not mouse_over_monster and time() - mt > 0.5 and DEBUGGING:
            mt = time()
            mx = mouse.get_position()[0]
            monsters.append(Hellhound(life=1, direction=[
                            "L", "R"][mx >= wn.width/2], x=mx))
        if mouse.is_button_pressed(3) and not mouse_over_monster and time() - mt > 0.5 and DEBUGGING:
            mt = time()
            mx = mouse.get_position()[0]
            monsters.append(
                Skelly(life=choice([1, 2, 3, 4]), direction=["L", "R"][mx >= wn.width/2], x=mx))
        # Fim debug

        wn.update()


if __name__ == "__main__":
    play(Window(1143, 768), 1)
