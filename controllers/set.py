# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from set.py")

def new():
    themes = getAllThemeWithCount()
    subthemes = getAllSubthemeWithCount()
    age_ranges = getAllAgeRangeWithCount()
    return dict(themes = themes, subthemes = subthemes, age_ranges = age_ranges)
