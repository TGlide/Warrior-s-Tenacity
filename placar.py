from helpers import *

# PPlay dependencies
from PPlay.font import *
from PPlay.window import *

def placar(wn):
    with open("placar.txt", "r") as f:
        x = sorted([i for i in f.readlines() if len(i.split()) == 2], key = lambda x: -int(x.split(" ")[1]))
        scores = [Font(line.replace("\n", ""), font_family=font_path("arcadeclassic"), size=75, 
        color=(255,255,255), local_font=True) for line in x]
    for score in range(3 if len(scores)>= 3 else len(scores)):
        scores[score].set_position(wn.width/2 - scores[score].width/2, 270 + score*(scores[0].height + 10))
    
    while True:
        wn.set_background_color((0,0,0))

        for score in range(3 if len(scores)>= 3 else len(scores)):
            scores[score].draw()

        if wn.get_keyboard().key_pressed("esc"):
            return

        wn.update()

if __name__ == "__main__":
    placar(Window(1200, 900))