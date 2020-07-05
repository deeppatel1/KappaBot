#!/usr/bin/python

from PIL import Image
import sys

try:
    league = Image.open("teams/lcs.png")
    team1 = Image.open("teams/tsm.png")
    team2 = Image.open("teams/t1.png")
except IOError:
    print("Unable to load image")
    sys.exit(1)

def get_concat(league, im1, im2):

    dst = Image.new('RGB', (im1.width + im2.width + league.width + 15, im1.height))
    dst.paste(league, (0, 0))
    dst.paste(im1, (im1.width, 0))
    dst.paste(im2, (im1.width + im2.width, 0))w
    return dst

get_concat(league, team1, team2).save('pillow_concat_h.jpg', format="JPEG", subsampling=0, quality=100)