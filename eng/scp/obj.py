from scp.utl import *
from scp.fnc import *

from numba import njit as nit, prange as prg
from random import randrange as rr
from numpy import zeros as zer

@nit
def dct_fce(dct_fce_dat, dct_fce_pic):
    dct_fce_lop = [dct_fce_dat.shape[0] - dct_fce_pic.shape[0], dct_fce_dat.shape[1] - dct_fce_pic.shape[1]]
    dct_fce_het = zer((dct_fce_lop[0], dct_fce_lop[1]))
    dct_fce_tol = 25
 
    for y in prg(dct_fce_lop[1]):
        for x in prg(dct_fce_lop[0]):
            dct_fce_het_cur = 0

            for a in prg(dct_fce_pic.shape[1]):
                for b in prg(dct_fce_pic.shape[0]):
                    dct_fce_chk = [False, False, False]

                    for c in range(3):
                        if dct_fce_dat[x + b, y + a][c] >= dct_fce_pic[b, a][c] - dct_fce_tol and dct_fce_dat[x + b, y + a][c] <= dct_fce_pic[b, a][c] + dct_fce_tol:
                            dct_fce_chk[c] = True
                    
                    if dct_fce_chk == [True, True, True]:
                        dct_fce_het_cur += 1
                        
            dct_fce_het[x, y] = dct_fce_het_cur / (dct_fce_lop[0] * dct_fce_lop[1])
    
    dct_fce_xy = (0, 0)
    dct_fce_stp = 0
    
    for y in prg(dct_fce_het.shape[1]):
        for x in prg(dct_fce_het.shape[0]):
            if dct_fce_het[x, y] > dct_fce_stp:
                dct_fce_stp = dct_fce_het[x, y]
                dct_fce_xy = (y, x)
            
    return dct_fce_xy

@nit
def fst_fce(fst_fce_dat, fst_fce_pic):
    fst_fce_sec = (fst_fce_dat.shape[0] // fst_fce_pic.shape[0], fst_fce_dat.shape[1] // fst_fce_pic.shape[1])
    fst_fce_sec_het = zer(fst_fce_sec)

    fst_fce_tol = 25

    for y in prg(fst_fce_sec[1]):
        for x in prg(fst_fce_sec[0]):
            fst_fce_sec_per = 0

            for b in prg(fst_fce_pic.shape[1]):
                for a in prg(fst_fce_pic.shape[0]):
                    fst_fce_sec_clr = [False, False, False]

                    for c in prg(3):
                        if fst_fce_dat[x * fst_fce_pic.shape[0] + a, y * fst_fce_pic.shape[1] + b][c] >= fst_fce_pic[a, b][c] - fst_fce_tol and fst_fce_dat[x * fst_fce_pic.shape[0] + a, y * fst_fce_pic.shape[1] + b][c] <= fst_fce_pic[a, b][c] + fst_fce_tol:
                            fst_fce_sec_clr[c] = True
                    
                    if fst_fce_sec_clr == [True, True, True]:
                        fst_fce_sec_per += 1
            
            fst_fce_sec_het[x, y] = fst_fce_sec_per / (fst_fce_pic.shape[0] * fst_fce_pic.shape[1])
    
    fst_fce_rug_xy = (0, 0)
    fst_fce_rug_sep = 0

    for y in prg(fst_fce_sec[1]):
        for x in prg(fst_fce_sec[0]):
            if fst_fce_sec_het[x, y] > fst_fce_rug_sep:
                fst_fce_rug_xy = (x * fst_fce_pic.shape[0], y * fst_fce_pic.shape[1])
                fst_fce_rug_sep = fst_fce_sec_het[x, y]
    
    fst_fce_smt_ara = (fst_fce_pic.shape[0] * 3, fst_fce_pic.shape[1] * 3)
    fst_fce_smt_het = zer(fst_fce_smt_ara)

    for y in prg(fst_fce_smt_ara[1]):
        for x in prg(fst_fce_smt_ara[0]):
            fst_fce_smt_per = 0

            for b in prg(fst_fce_pic.shape[1]):
                for a in prg(fst_fce_pic.shape[0]):
                    fst_fce_smt_clr = [False, False, False]

                    for c in prg(3):
                        if fst_fce_dat[fst_fce_rug_xy[0] - fst_fce_pic.shape[0] + x + a, fst_fce_rug_xy[1] - fst_fce_pic.shape[1] + y + b][c] >= fst_fce_pic[a, b][c] - fst_fce_tol and fst_fce_dat[fst_fce_rug_xy[0] - fst_fce_pic.shape[0] + x + a, fst_fce_rug_xy[1] - fst_fce_pic.shape[1] + y + b][c] <= fst_fce_pic[a, b][c] + fst_fce_tol:
                            fst_fce_smt_clr[c] = True
                    
                    if fst_fce_smt_clr == [True, True, True]:
                        fst_fce_smt_per += 1
            
            fst_fce_smt_het[x, y] = fst_fce_smt_per / (fst_fce_pic.shape[0] * fst_fce_pic.shape[1])

    fst_fce_smt_xy = (0, 0)
    fst_fce_smt_sep = 0

    for y in prg(fst_fce_smt_ara[1]):
        for x in prg(fst_fce_smt_ara[0]):
            if fst_fce_smt_het[x, y] > fst_fce_smt_sep:
                fst_fce_smt_xy = (y, x)
                fst_fce_smt_sep = fst_fce_smt_het[x, y]

    return (fst_fce_rug_xy[1] - fst_fce_pic.shape[1] + fst_fce_smt_xy[0], fst_fce_rug_xy[0] - fst_fce_pic.shape[0] + fst_fce_smt_xy[1]), fst_fce_smt_sep