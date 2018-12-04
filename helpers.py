import os, sys

def font_path(name):
    idx = os.path.realpath(__file__).find("helpers.py")
    return os.path.realpath(__file__)[:idx] + "assets" + os.sep + "fonts" + os.sep + name + ".ttf"

def get_asset(name):
    idx = os.path.realpath(__file__).find("helpers.py")
    return os.path.realpath(__file__)[:idx] + "assets" + os.sep + name 

def get_sprite(name):
    return get_asset("sprites" + os.sep + name)

def get_sfx(name):
    return get_asset("sounds" + os.sep + name)