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

def dst(xy_1, xy_2):
    return (abs(xy_2[0] - xy_1[0]) ** 2 + abs(xy_2[1] - xy_1[1]) ** 2) ** (1 / 2)

# data

def jsn(loc):
    return lod(open(loc))

# color

def cfg(clr):
    return (clp(int(clr[0]), 0, 255), clp(int(clr[1]), 0, 255), clp(int(clr[2]), 0, 255))

def flp(clr):
    clr = cfg(clr)
    return (255 - clr[0], 255 - clr[1], 255 - clr[2])