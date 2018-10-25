import time

from helpers import *

# PPlay dependencies
from PPlay.font import *
from PPlay.window import *

def dificuldade(wn):
	dificul = Font("Dificuldade", font_family=font_path("futilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	dificul.set_position(wn.width/2 - dificul.width/2, wn.height/4 - 100)

	facil = Font("Fácil", font_family=font_path("futilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	facil.set_position(wn.width/2 - facil.width/2, wn.height/3 - 50)

	medio = Font("Médio", font_family=font_path("futilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	medio.set_position(wn.width/2 - medio.width/2, facil.y + facil.height + 50)

	dificil = Font("Difícil", font_family=font_path("futilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	dificil.set_position(wn.width/2 - dificil.width/2, medio.y + medio.height + 50)



	options = [facil, medio, dificil]

	selection_arrow = Font(">", font_family=font_path("futilePro"),
              size=100, color=(255, 255, 255), local_font=True)
	selection_idx = 0
	selection_time_counter = time.time()

	while True:
		wn.set_background_color((0,0,0))
		
		dificul.draw()
		for option in options:
			option.draw()

		if time.time() - selection_time_counter >= 0.125: # Impede alternar entre seleções muito rapidamente
			selection_time_counter = time.time()
			if window.Window.get_keyboard().key_pressed("up"):
				selection_idx = [len(options)-1, selection_idx - 1][selection_idx > 0]
			elif window.Window.get_keyboard().key_pressed("down"):
				selection_idx = (selection_idx + 1) % len(options)
			elif window.Window.get_keyboard().key_pressed("enter"):
				return selection_idx + 1
		
		selection = options[selection_idx]
		selection_arrow.set_position(selection.x - selection_arrow.width, selection.y)
		selection_arrow.draw()

		wn.update()