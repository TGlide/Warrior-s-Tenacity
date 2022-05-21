# -*- coding: utf-8 -*-

import time

from helpers import *

# PPlay dependencies
from PPlay.font import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import *


def menu(wn):
	title = GameImage(get_asset("logo.png"), ( int((1280*(wn.height/2))/720), int(wn.height/2)))
	title.set_position(wn.width/2 - title.width/2, 20)

	play=Font("Play", font_family=font_path("FutilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	play.set_position(wn.width/2 - play.width/2, title.y + title.height)

	dificuldade=Font("Placar", font_family=font_path("FutilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	dificuldade.set_position(
	    wn.width/2 - dificuldade.width/2, play.y + play.height + 20)

	placar=Font("Sair", font_family=font_path("FutilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	placar.set_position(wn.width/2 - placar.width/2,
	                    dificuldade.y + dificuldade.height + 20)

	sair=Font("Sair", font_family=font_path("FutilePro"),
              size=75, color=(255, 255, 255), local_font=True)
	sair.set_position(wn.width/2 - sair.width/2,
	                  dificuldade.y + dificuldade.height + 20)
    
	options=[play, dificuldade, placar]

	selection_arrow=Font(">", font_family=font_path("FutilePro"),
              size=100, color=(255, 255, 255), local_font=True)
	selection_idx=0
	selection_time_counter=time.time()

	mouse = wn.get_mouse()
	while True:
		wn.set_background_color((0, 0, 0))

		title.draw()
		selection_idx = -1
		for option in options:
			option.draw()
			if mouse.is_over_object(option):
					selection_idx = options.index(option)

		if selection_idx != -1:
			selection=options[selection_idx]
			selection_arrow.set_position(
				selection.x - selection_arrow.width - 10, selection.y)
			selection_arrow.draw()
			
			if time.time() - selection_time_counter >= 0.125 and mouse.is_button_pressed(1):  # Impede alternar entre seleções muito rapidamente
				selection_time_counter=time.time()
				if selection_idx != -1:
					return selection_idx

		wn.update()
