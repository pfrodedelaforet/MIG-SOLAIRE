import numpy.random as rd
import matplotlib.pyplot as plt

class Triporteur:
    def __init__(self,capacity,dispo,position):
        self.capacity = capacity #flottant : poids qu'il peut porter
        self.dispo = dispo #booleen : le triporteur est prêt à partir
        self.position = position #point
    def __repr__(self):
        str(self.capacity,self.dispo,self.position)
class pt:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x},{self.y})"

def random_float(a,b):
    return (rd.random() * (b-a)) + a

def random_pt(a,b):
    return pt(random_float(a,b),random_float(a,b))

def dist(i,j):
    return ((i.x - j.x)**2 + (i.y - j.y)**2)**0.5

def flatten(l):
    nl = []
    for i in l:
        nl = nl + i
    return(nl)

def s(pts,i,j):
    return(dist(pts[i],pts[0]) + dist(pts[0],pts[j]) - dist(pts[i],pts[j]))

def delkey(d,k):
    if k in d:
        del d[k]
        
def merge(pts,i,j,sw,ew):#sw et ew sont définis dans Clarke, on fusionne la route qui finit par i avec celle qui commence par j
    (r1,p1),(r2,p2) = ew[i],sw[j]
    si,ej = r1[0],r2[-1]
    delkey(ew,i)
    delkey(ew,ej)
    delkey(sw,si)
    delkey(sw,j)
    nr = r1 + r2
    np = p1 + p2 - s(pts,i,j)
    ew[ej] = (nr,np)
    sw[si] = (nr,np)

def poids_fus(pts,i,j,sw,ew):
    return ew[i][1] + sw[j][1] - s(pts,i,j)

def Clarke(pts,k):#pts[0] est le dépot, les autres sont les points correspondant aux clients
    n = len(pts)
    tournees = n-1
    gains = flatten([[((i,j),s(pts,i,j)) for i in range(1,n) if i != j] for j in range(1,n)])
    gains.sort(key = lambda x: x[1],reverse = True)
    sw = {} #sw[i] : la route qui commence par i
    ew = {} #ew[i] : la route qui termine par i
    for i in range(1,n):
        sw[i] = ([i],dist(pts[0],pts[i])+dist(pts[i],pts[0])) #Les routes sont des couples : famille de points : qui indique le chemin, et poids de la route: que ce soit en kg / energie / temps......... on peut l'adapter en modifiant dist
        ew[i] = ([i],dist(pts[0],pts[i])+dist(pts[i],pts[0]))
    while tournees > k:
        (i,j),sij = gains[0]
        if i in ew and j in sw and j != ew[i][0][0]:
            a = ew[i][0][0]
            b = sw[j][0][-1]
            merge(pts,i,j,sw,ew)
            tournees -=1
        else:
            del gains[0]
        
    l = []
    for i in sw.values():
        l.append(i[0])
    return(l)

def itobi(pts,ipl):
    x = []
    y = []
    for i in ipl:
        x.append(pts[i].x)
        y.append(pts[i].y)
    return(x,y)

def test(n,k,a=-1,b=1):
    pts = [random_pt(a,b) for i in range(n+1)]
    cp = Clarke(pts,k)
    for i in cp:
        i.append(0)
        i.insert(0,0)
    xs = []
    ys = []
    for i in cp:
        x,y = itobi(pts,i)
        xs.append(x)
        ys.append(y)
    for x,y in zip(xs,ys):
        plt.plot(x,y)
    plt.show()
