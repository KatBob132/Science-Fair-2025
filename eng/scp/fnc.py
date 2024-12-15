from json import load as lod

# math

def clp(num, min=None, max=None):
    if min != None:
        if num < min:
            num = min
    if max != None:
        if num > max:
            num = max
    
    return num

def xy_avg(lit):
    lit = list(lit)
    avg = [0, 0]

    for elm in lit:
        for a in range(2):
            avg[a] += elm[a]
    
    for a in range(2):
        avg[a] /= len(lit)

    return avg

def dst(xy_1, xy_2):
    return (abs(xy_2[0] - xy_1[0]) ** 2 + abs(xy_2[1] - xy_1[1]) ** 2) ** (1 / 2)

# data

def jsn_dat(loc):
    return lod(open(loc))

# color

def cfg_clr(clr):
    return (clp(int(clr[0]), 0, 255), clp(int(clr[1]), 0, 255), clp(int(clr[2]), 0, 255))

def flp_clr(clr):
    clr = cfg_clr(clr)

    return (255 - clr[0], 255 - clr[1], 255 - clr[2])

def bld_clr(clr_1, clr_2, clr_phs):
    bld_d_clr = []

    for a in range(3):
        bld_d_clr.append(clr_1[a] + (clr_2[a] - clr_1[a]) * clr_phs)

    return cfg_clr(bld_d_clr)