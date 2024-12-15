from scp.obj import *
from scp.utl import *
from scp.fnc import *

from pygame.locals import *

import pygame.camera as cam_pg
import pygame as pg

from time import time as tme
from sys import exit as ext

pg.init()
pg.camera.init()

cam = {}

cam["fed"] =  cam_pg.Camera(cam_pg.list_cameras()[0])
cam["fed"].start()

cam["siz"] = cam["fed"].get_size()
cam["rez"] = 1
cam["rlz"] = (cam["siz"][0] // cam["rez"], cam["siz"][1] // cam["rez"])

cam["img"] = cam["fed"].get_image()
cam["srf"] = pg.Surface(cam["siz"])

cam["mat"] = []

for y in range(cam["rlz"][1]):
    cam["mat"].append([])

    for x in range(cam["rlz"][0]):
        cam["mat"][y].append([[0, 0, 0], 0])

clr = jsn_dat("eng/dat/clr.json")
scn = {}

scn["siz"] = cam["rlz"]
scn["pix-siz"] = 2

scn["srf"] = pg.Surface(scn["siz"])

scn["win"] = None
scn["win-bck"] = None

siz = (scn["siz"][0] * scn["pix-siz"], scn["siz"][1] * scn["pix-siz"])
txt = txt_utl("eng/dat/fnt.json", scn["srf"])

tme_cal = {}
fps_cal = {}

tme_cal["str"] = tme()
tme_cal["now"] = 0
tme_cal["dlt"] = 0

fps_cal["fps"] = 0
fps_cal["fps-lit"] = []
fps_cal["fps-avg"] = 0

mov = {}

dpy = pg.display.set_mode(siz, DOUBLEBUF)
pg.display.set_caption("Motion")
fps = pg.time.Clock()

mos_dat = {}

mos_dat["xy"] = [pg.mouse.get_pos()[0] // scn["pix-siz"], pg.mouse.get_pos()[1] // scn["pix-siz"]]
mos_dat["btt"] = [False, False, False]

while True:
    dpy.fill(clr["white"])
    scn["srf"].fill(clr["white"])

    for a in range(2):
        mos_dat["xy"][a] = pg.mouse.get_pos()[a] // scn["pix-siz"]

    tme_cal["now"] = tme()
    tme_cal["dlt"] = clp(tme_cal["now"] - tme_cal["str"], 0.000000000000000001)
    tme_cal["str"] = tme()

    fps_cal["fps"] = 1 / tme_cal["dlt"]
    fps_cal["fps-lit"].append(fps_cal["fps"])

    if len(fps_cal["fps-lit"]) > round(fps_cal["fps"]):
        fps_cal["fps-lit"].pop(0)
    
    fps_cal["fps-avg"] = round(sum(fps_cal["fps-lit"]) / len(fps_cal["fps-lit"]))

    cam["img"] = cam["fed"].get_image()
    cam["srf"].blit(cam["img"], (0, 0))
    scn["srf"].blit(pg.transform.scale(cam["srf"], scn["siz"]), (0, 0))

    # mov["ary"] = pg.PixelArray(scn["srf"])

    # for y in range(cam["rlz"][1]):
    #     for x in range(cam["rlz"][0]):
    #         mov["xy"] = pg.Color(mov["ary"][x, y])

    txt.drw(str(fps_cal["fps-avg"]), 2, (2, 2), clr["red"])

    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            pg.quit()
            ext()

        if evt.type == pg.KEYDOWN:            
            if evt.key == pg.K_ESCAPE:
                pg.quit()
                ext()            

        if evt.type == pg.MOUSEBUTTONDOWN:
            for a in range(3):
                if evt.button == a + 1:
                    mos_dat["btt"][a] = True

        if evt.type == pg.MOUSEBUTTONUP:
            for a in range(3):
                if evt.button == a + 1:
                    mos_dat["btt"][a] = False
        
    scn["win"] = pg.transform.scale(scn["srf"], siz)
    scn["win-bck"] = pg.transform.scale(scn["srf"], siz)

    scn["win-bck"].set_alpha(51)

    dpy.blit(scn["win"], (0, 0))
    dpy.blit(scn["win-bck"], (scn["pix-siz"], scn["pix-siz"]))

    pg.display.update() 
    pg.display.flip()
    fps.tick(0)