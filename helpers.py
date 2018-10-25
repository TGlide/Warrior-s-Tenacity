import os, sys

def font_path(name):
    return os.path.realpath(__file__)[:-(len("helpers.py"))] + "assets" + os.sep + "fonts" + os.sep + name + ".ttf"

def get_asset(name):
    return os.path.realpath(__file__)[:-(len("helpers.py"))] + "assets" + os.sep + name 