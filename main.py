from Screens import Screens
import os
import pygame

colors = [("DARKRED", 162, 0, 0), ("DARKBLUE", 0, 100, 185), ("GRAY2", 240, 240, 240), ("BORDER_GRAY", 100, 100, 100), ("LIGHT_GRAY", 190, 190, 190), ("GRAY_SHADE", 170, 170, 170), ("GREEN", 0, 255, 0), ("BLACK", 0, 0, 0), ("WHITE", 255, 255, 255), ("GRAY", 230, 230, 230), ("BLUE", 0, 162, 237), ("LIGHTBLUE", 41, 187, 255), ("RED", 199, 62, 29), ("LIGHTRED", 255, 88, 85)]
codes = [("IDLE", -1), ("ACTION_SOLVE", 0), ("ACTION_REFRESH", 1), ("ACTION_DISABLE_ALL", 2), ("ACTION_SELECT", 3), ("ACTION_KEYPRESS", 4)]

"""
Build_path_with_cwd(paths) concatenates the current working directory with
each path in paths and returns the new list.
"""
def build_path_with_cwd(paths):
    return [os.getcwd() + path for path in paths]

"""
Build_color_dictionary(colors) converts the list of color tuples into a corresponding 
Dictionary object and returns it.
"""
def build_color_dictionary(colors):
    res = dict()
    for i in range(len(colors)):
            res[colors[i][0]] = colors[i][1:4]
    return res

"""
Build_code_dictionary(codes) converts the list of code tuples into a corresponding
Dictionary object and returns it.
"""
def build_code_dictionary(codes):
    res = dict()
    for j in range(len(codes)):
        res[codes[j][0]] = codes[j][1]
    return res

paths = build_path_with_cwd(["/sudoku-solver/images/bgs/grid.png", "/sudoku-solver/images/icons/refresh.png", "/sudoku-solver/images/icons/logo.png", "/sudoku-solver/images/icons/prev-step.png"])
colors = build_color_dictionary(colors)
codes = build_code_dictionary(codes)
data = {'colors': colors, 'codes': codes, 'paths': paths}
screenUtil = Screens(data)
screenUtil.START.handle_event()


