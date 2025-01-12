from scp.obj import *
from scp.utl import *
from scp.fnc import *

from pygame.locals import *

import pygame.camera as cam_pg
import pygame as pg

from numpy import array as ary
from time import time as tme
from sys import exit as ext

pg.init()
pg.camera.init()

cam = {}

cam["fed"] =  cam_pg.Camera(cam_pg.list_cameras()[0])
cam["fed"].start()

cam["siz"] = cam["fed"].get_size()
cam["rez"] = 3
cam["rlz"] = (cam["siz"][0] // cam["rez"], cam["siz"][1] // cam["rez"])

cam["img"] = cam["fed"].get_image()
cam["srf"] = pg.Surface(cam["siz"])

cam["mat"] = []

for y in range(cam["rlz"][1]):
    cam["mat"].append([])

    for x in range(cam["rlz"][0]):
        cam["mat"][y].append([[0, 0, 0], 0])

clr = jsn("eng/dat/clr.json")
scn = {}

scn["siz"] = cam["rlz"]
scn["pix-siz"] = 5

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

fce = {}

fce["pic"] = {}

fce["pic"]["siz"] = (0, 0)
fce["pic"]["dat"] = []

fce["xy"] = [0, 0]
fce["dat"] = []

for y in range(cam["rlz"][1]):
    fce["dat"].append([])

    for x in range(cam["rlz"][0]):    
        fce["dat"][y].append((0, 0, 0))

dpy = pg.display.set_mode(siz, DOUBLEBUF)
pg.display.set_caption("Motion")
fps = pg.time.Clock()

mos_dat = {}

mos_dat["xy"] = [pg.mouse.get_pos()[0] // scn["pix-siz"], pg.mouse.get_pos()[1] // scn["pix-siz"]]
mos_dat["btt"] = [False, False, False]

mos_dat["hld"] = []
mos_dat["hld_xy"] = [(0, 0), (0, 0)]

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

    for y in prg(cam["rlz"][1]):
        for x in prg(cam["rlz"][0]):
            fce["dat"][y][x] = scn["srf"].get_at((x, y))
            fce["dat"][y][x] = [fce["dat"][y][x].r, fce["dat"][y][x].g, fce["dat"][y][x].b]

            for a in prg(3):
                fce["dat"][y][x][a] = clp(fce["dat"][y][x][a] * 1.1, 0, 255)
                fce["dat"][y][x][a] = fce["dat"][y][x][a] // 5 * 5

    if fce["pic"]["siz"][0] != 0:
        fce["fce"] = fst_fce(ary(fce["dat"]), ary(fce["pic"]["dat"]))

        txt.drw(str(round(fce["fce"][1] * 100, 2)) + "%", 1, (1, 9), clr["white"], (0, 1), clr["black"])

        for y in range(fce["pic"]["siz"][1]):
            for x in range(fce["pic"]["siz"][0]):
                if x == 0 or x == fce["pic"]["siz"][0] - 1 or y == 0 or y == fce["pic"]["siz"][1] - 1:
                    pg.draw.rect(scn["srf"], flp(fce["dat"][fce["fce"][0][1] + y][fce["fce"][0][0] + x]), pg.Rect(fce["fce"][0][0] + x, fce["fce"][0][1] + y, 1, 1))

    pg.draw.rect(scn["srf"], clr["red"], pg.Rect(mos_dat["hld_xy"][0][0], mos_dat["hld_xy"][0][1], mos_dat["hld_xy"][1][0] - mos_dat["hld_xy"][0][0], mos_dat["hld_xy"][1][1] - mos_dat["hld_xy"][0][1]), 1)

    txt.drw(str(fps_cal["fps-avg"]), 1, (1, 1), clr["white"], (0, 1), clr["black"])

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
    
    mos_dat["hld"].append(mos_dat["btt"][0])

    if len(mos_dat["hld"]) > 2:
        mos_dat["hld"].pop(0)
    if len(mos_dat["hld"]) == 2:
        if mos_dat["hld"][0] == False and mos_dat["hld"][1]:
            mos_dat["hld_xy"][0] = (mos_dat["xy"][0], mos_dat["xy"][1])
        elif mos_dat["hld"][0] and mos_dat["hld"][1]:
            mos_dat["hld_xy"][1] = (mos_dat["xy"][0], mos_dat["xy"][1])
        elif mos_dat["hld"][0] and mos_dat["hld"][1] == False:
            fce["pic"]["siz"] = (abs(mos_dat["hld_xy"][1][0] - mos_dat["hld_xy"][0][0]), abs(mos_dat["hld_xy"][1][1] - mos_dat["hld_xy"][0][1]))
            fce["pic"]["dat"] = []

            for y in range(fce["pic"]["siz"][1]):
                fce["pic"]["dat"].append([])

                for x in range(fce["pic"]["siz"][0]):
                    fce["pic"]["dat"][y].append(fce["dat"][mos_dat["hld_xy"][0][1] + y][mos_dat["hld_xy"][0][0] + x])
        else:
            mos_dat["hld_xy"] = [(0, 0), (0, 0)]

    scn["win"] = pg.transform.scale(scn["srf"], siz)
    scn["win-bck"] = pg.transform.scale(scn["srf"], siz)
    scn["win-bck"].set_alpha(51)

    dpy.blit(scn["win"], (0, 0))
    dpy.blit(scn["win-bck"], (scn["pix-siz"], scn["pix-siz"]))

    pg.display.update() 
    pg.display.flip()
    fps.tick(0)