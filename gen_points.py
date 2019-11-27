import numpy as np
import numpy.random as rd
import pandas as pd

def rand_float(a=-1,b=1):
    r = rd.random()
    return a + (b-a)*r

def generer(k):
    l = []
    for i in range(k):
        l.append(f"[{rand_float()}:{rand_float()}]")
    return l

def ecrire():
    nbs = [10*i for i in range(1,11)]
    f = open("points.txt", "w")
    for i in range(len(nbs)-1):
        gi = generer(nbs[i])
        for j in range(len(gi)-1):
            f.write(gi[j])
            f.write(',')
        f.write(str(gi[len(gi)-1]))
        f.write('\n')
    gi = generer(nbs[len(nbs)-1])
    for j in range(len(gi)-1):
        f.write(gi[j])
        f.write(',')
    f.write(gi[len(gi)-1])
    f.close()

def to_couple(s):
    s1 = ""
    s2 = ""
    w1 = True
    for i in s:
        if not i in ['[',']']:
            if i == ':':
                w1 = False
            else:
                if w1:
                    s1 = s1 + i
                else:
                    s2 = s2 + i
    i1 = float(s1)
    i2 = float(s2)
    return(i1,i2)

def to_pt_list(l):
    nl = []
    for i in l:
        nl.append(to_couple(i))
    return(nl)

def to_nb_array(fname):
    points = []
    f = open(fname,"r")
    for x in f:
        x = x.rstrip()
        points.append(x.split(","))
    
    return(list(map(to_pt_list,points)))
        
        
    
