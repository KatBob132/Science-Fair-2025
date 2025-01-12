from scp.fnc import *

import pygame as pg

class txt_utl:
    def __init__(self, txt_dat, txt_srf):
        self.txt_dat = jsn(txt_dat)
        self.txt_srf = txt_srf
    
    def ara(self, ara_txt, ara_siz, ara_sdw_plc=(0, 0)):
        self.ara_txt = str(ara_txt)
        self.ara_siz = int(ara_siz)
        self.ara_sdw_plc = (int(ara_sdw_plc[0]), int(ara_sdw_plc[1]))

        self.ara_spc = [0, 0]

        for a in range(len(self.ara_txt)):
            self.ara_spc[0] += len(self.txt_dat[self.ara_txt[a]][0]) * self.ara_siz + self.ara_siz

            if a < len(self.ara_txt) - 1:
                self.ara_spc[0] += self.ara_sdw_plc[0]

            if self.ara_spc[1] < len(self.txt_dat[self.ara_txt[a]]) * self.ara_siz + self.ara_sdw_plc[1]:
                self.ara_spc[1] = len(self.txt_dat[self.ara_txt[a]]) * self.ara_siz + self.ara_sdw_plc[1]
        
        return self.ara_spc

    def drw(self, drw_txt, drw_siz, drw_xy, drw_clr, drw_sdw_plc=(0, 0), drw_sdw_clr=(0, 0, 0), drw_cnr=(False, False)):
        self.drw_txt = str(drw_txt)

        self.drw_siz = int(drw_siz)
        self.drw_xy = (int(drw_xy[0])), int(drw_xy[1])
        self.drw_clr = cfg(drw_clr)
        
        self.drw_sdw_plc = (int(drw_sdw_plc[0]), int(drw_sdw_plc[1]))
        self.drw_sdw_clr = cfg(drw_sdw_clr)

        self.drw_cnr = (bool(drw_cnr[0]), bool(drw_cnr[1]))
        self.drw_cnr_val = self.ara(self.drw_txt, self.drw_siz, self.drw_sdw_plc)
        self.drw_cnr_add = [0, 0]

        for a in range(2):
            if self.drw_cnr[a]:
                self.drw_cnr_add[a] -= int(self.drw_cnr_val[a] / 2)

        self.drw_plc = 0

        for let in self.drw_txt:
            for y in range(len(self.txt_dat[let])):
                for x in range(len(self.txt_dat[let][0])):
                    if self.txt_dat[let][y][x] == 1:
                        if self.drw_sdw_plc != (0, 0):
                            pg.draw.rect(self.txt_srf, self.drw_sdw_clr, pg.Rect(self.drw_xy[0] + self.drw_plc + (x * self.drw_siz) + self.drw_sdw_plc[0] + self.drw_cnr_add[0], self.drw_xy[1] + (y * self.drw_siz) + self.drw_sdw_plc[1] + self.drw_cnr_add[1], self.drw_siz, self.drw_siz))

                        pg.draw.rect(self.txt_srf, self.drw_clr, pg.Rect(self.drw_xy[0] + self.drw_plc + (x * self.drw_siz) + self.drw_cnr_add[0], self.drw_xy[1] + (y * self.drw_siz) + self.drw_cnr_add[1], self.drw_siz, self.drw_siz))
            
            self.drw_plc += len(self.txt_dat[let][0]) * self.drw_siz + self.drw_siz + self.drw_sdw_plc[0]