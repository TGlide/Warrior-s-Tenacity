import os
import random

from PPlay.window import *
from menu import menu
from play2 import play
from dificuldade import dificuldade

##################
# GAME CONSTANTS #
##################

WIN_W = 1143
WIN_H = 768
DIFICULDADE = 1

#############
# Execution #
#############
wn = Window(WIN_W, WIN_H)
while True:
	selec = menu(wn)
	if selec == 0: 
		play(wn, DIFICULDADE)
	elif:
		break


