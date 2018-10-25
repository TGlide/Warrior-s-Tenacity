from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from time import sleep, time
from os import getcwd
from random import choice
from helpers import *


def play(wn, difficulty):
    class Ein:

        def __init__(self, x, y):
            # Sprites for all different states for Ein
            self.sprites = {
                "idle": Sprite(get_asset("ein%sein_idle_left.png" % os.sep), 4),
                "walk": Sprite(get_asset("ein%sein_walking_left.png" % os.sep), 6),
            }

            self.last_sprite = "idle"  # This is needed for resetting the frames when chaning states
            self.current_sprite = "idle"

            self.x = x - self.sprites['idle'].width/2
            self.y = y - self.sprites['idle'].height

            self.orientation = "R"

            for s in self.sprites:
                self.sprites[s].set_position(self.x, self.y)
                self.sprites[s].set_total_duration(1000)

        def move_key_x(self, speed):
            if Window.get_keyboard().key_pressed("left"):
                self.current_sprite = "walk"
                self.orientation = "L"
                self.x -= speed
            elif Window.get_keyboard().key_pressed("right"):
                self.current_sprite = "walk"
                self.orientation = "R"
                self.x += speed
            else:
                self.current_sprite = "idle"

        def reset_frames(self):
            for s in self.sprites:
                self.sprites[s].set_curr_frame = 0

        def update(self):
            self.sprites[self.current_sprite].set_position(self.x, self.y)
            if self.current_sprite != self.last_sprite:
                self.reset_frames()
                self.last_sprite = self.current_sprite
            else:
                self.sprites[self.current_sprite].update()

        def draw(self):
            self.sprites[self.current_sprite].draw(
                flip=self.orientation == "R")

        def getwidth(self):
            return self.sprites[self.current_sprite].width

    class Skelly:
        spawn_interval = 5/difficulty

        def __init__(self, x, y, orientation):
            # Sprites for all different states for Ein
            self.sprites = {
                "idle": Sprite(get_asset("skelly%sidle.png" % os.sep), 11, size=(907, 110)),
                "walk": Sprite(get_asset("skelly%swalk.png" % os.sep), 13, size=(953, 110)),
            }

            self.last_sprite = "walk"  # This is needed for resetting the frames when chaning states
            self.current_sprite = "walk"

            self.x = x - self.sprites['idle'].width/2
            self.y = y - self.sprites['idle'].height

            self.orientation = orientation

            for s in self.sprites:
                self.sprites[s].set_position(self.x, self.y)
                self.sprites[s].set_total_duration(1000)

        def move(self, speed, ein):
            if self.orientation == "R":
                if self.x + self.sprites[self.current_sprite].width < ein.x - 50:
                    self.x += speed
                else:
                    self.current_sprite = "idle"
            else:
                if self.x > ein.x + ein.getwidth():
                    self.x -= speed
                else:
                    self.current_sprite = "idle"

        def reset_frames(self):
            for s in self.sprites:
                self.sprites[s].set_curr_frame = 0

        def update(self):
            self.sprites[self.current_sprite].set_position(self.x, self.y)
            if self.current_sprite != self.last_sprite:
                self.reset_frames()
                self.last_sprite = self.current_sprite
            else:
                self.sprites[self.current_sprite].update()

        def draw(self):
            self.sprites[self.current_sprite].draw(
                flip=self.orientation == "L")

    class Hellhound:
        spawn_interval = 2/difficulty

        def __init__(self, x, y, orientation):
            # Sprites for all different states for Ein
            self.sprites = {
                "idle": Sprite(get_asset("hellhound{0}PNG{0}idle.png".format(os.sep)), 6, size=(1320, 110)),
                "walk": Sprite(get_asset("hellhound{0}PNG{0}walk.png".format(os.sep)), 12, size=(2640, 110)),
            }

            self.last_sprite = "walk"  # This is needed for resetting the frames when chaning states
            self.current_sprite = "walk"

            self.x = x - self.sprites['idle'].width/2
            self.y = y - self.sprites['idle'].height

            self.orientation = orientation

            for s in self.sprites:
                self.sprites[s].set_position(self.x, self.y)
                self.sprites[s].set_total_duration(1000)

        def move(self, speed, ein):
            if self.orientation == "R":
                if self.x + self.sprites[self.current_sprite].width < ein.x - 50:
                    self.x += speed
                else:
                    self.current_sprite = "idle"
            else:
                if self.x > ein.x + ein.getwidth():
                    self.x -= speed
                else:
                    self.current_sprite = "idle"

        def reset_frames(self):
            for s in self.sprites:
                self.sprites[s].set_curr_frame = 0

        def update(self):
            self.sprites[self.current_sprite].set_position(self.x, self.y)
            if self.current_sprite != self.last_sprite:
                self.reset_frames()
                self.last_sprite = self.current_sprite
            else:
                self.sprites[self.current_sprite].update()

        def draw(self):
            self.sprites[self.current_sprite].draw(
                flip=self.orientation == "R")

    class Knight:
        spawn_interval = 3/difficulty

        def __init__(self, x, y, orientation):
            # Sprites for all different states for Ein
            self.sprites = {
                "idle": Sprite(get_asset("knight{0}idle.png".format(os.sep)), 4, size=(440, 110)),
                "walk": Sprite(get_asset("knight{0}walk.png".format(os.sep)), 8, size=(880, 110)),
            }

            self.last_sprite = "walk"  # This is needed for resetting the frames when chaning states
            self.current_sprite = "walk"

            self.x = x - self.sprites['idle'].width/2
            self.y = y - self.sprites['idle'].height

            self.orientation = orientation

            for s in self.sprites:
                self.sprites[s].set_position(self.x, self.y)
                self.sprites[s].set_total_duration(1000)

        def move(self, speed, ein):
            if self.orientation == "R":
                if self.x + self.sprites[self.current_sprite].width < ein.x - 50:
                    self.x += speed
                else:
                    self.current_sprite = "idle"
            else:
                if self.x > ein.x + ein.getwidth():
                    self.x -= speed
                else:
                    self.current_sprite = "idle"

        def reset_frames(self):
            for s in self.sprites:
                self.sprites[s].set_curr_frame = 0

        def update(self):
            self.sprites[self.current_sprite].set_position(self.x, self.y)
            if self.current_sprite != self.last_sprite:
                self.reset_frames()
                self.last_sprite = self.current_sprite
            else:
                self.sprites[self.current_sprite].update()

        def draw(self):
            self.sprites[self.current_sprite].draw(
                flip=self.orientation == "L")

    ####################
    # Global Variables #
    ####################
    FLOOR_Y = (510*wn.height)/643
    SPAWN_INTERVAL = 5/difficulty
    MAX_ENEMIES = 3*difficulty
    ENEMY_SPEED = 0.5*difficulty

    ########
    # Main #
    ########
    fundo = GameImage(get_asset("bg.png"), (wn.width, wn.height))

    danse = Sound(get_asset("danse.ogg"))
    danse.play()

    ein = Ein(wn.width/2, FLOOR_Y)

    enemies = {
        "Skelly": [],
        "Hellhound": [],
        "Knight": []
    }

    spawn_timer = time()
    # Game Loop
    while True:
        fundo.draw()

        for enemy_type in enemies:
            if time() - spawn_timer >= eval(enemy_type).spawn_interval and len(enemies[enemy_type]) < MAX_ENEMIES:
                spawn_timer = time()
                orient = choice(["L", "R"])
                en_x = [0, wn.width][orient == "L"]
                enemies[enemy_type].append(
                    eval(enemy_type)(en_x, FLOOR_Y, orient))
            for enemy in enemies[enemy_type]:
                enemy.move(ENEMY_SPEED, ein)
                enemy.draw()
                enemy.update()

        # ein.move_key_x(1)
        ein.update()

        ein.draw()

        wn.update()
