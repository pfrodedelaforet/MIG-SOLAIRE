from classes import *
import numpy as np

def s(clients,dist,i,j,elp): #C'est un Poids ,s permet l'optimisation des tournees c'est une matrice len(pts)² ,i et j sont des indices, clients une liste de DeliveryPoint
    #print(clients[i])
    #print(clients[j])
    return(dist(clients[i],elp) + dist(elp,clients[j]) - dist(clients[i],clients[j]))

#optimisation en utilisant une methode de TSP        
def cost_change(dst,pts,route, i,j):
    return dst(pts[route[i-1]],pts[route[j]]) + dst(pts[route[i]],pts[route[j+1]]) - (dst(pts[route[i-1]],pts[route[i]]) + dst(pts[route[j]],pts[route[j+1]]))


def two_opt(dst,pts,route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)-1):
                if cost_change(dst,pts,best, i, j) < 0:
                    best[i:j+1] = best[j:i - 1:-1]
                    improved = True
        route = best
#fin TSP

def separer(dst,elps,clients): #Sorte de Voronoi en n²
    seplist = [[elps[i]] for i in range(len(elps))]#le premier element de seplist[i] est le point correspondant à elp[i]
    for i in clients:
        d = [(dst(i,elps[j]),j) for j in range(len(elps))]
        elp = min(d,key = lambda x:x[0])[1]
        seplist[elp].append(i)
    return seplist

def flatten(l): #a Liste Liste  -> a Liste
    nl = []
    for i in l:
        nl = nl + i
    return(nl)

def delkey(d,k):
    if k in d:
        del d[k]
        
def merge(clients,i,j,sw,ew):#sw et ew sont des dictionnaires cles : indices ,value: tournee. On fusionne la route qui finit par i avec celle qui commence par j
    tourn1,tourn2 = ew[i],sw[j]
    si,ej = tourn1.indices[0],tourn2.indices[-1]
    delkey(ew,i)
    delkey(ew,ej)
    delkey(sw,si)
    delkey(sw,j)
    ntourn = tourn1 + tourn2
    ew[ej] = ntourn
    sw[si] = ntourn
    
def req(triporteur,tourn,t0):
    return(tourn.masse <= triporteur.capacity and all(list(map(lambda x: tourn.clients[x].t1 <= t0 + tourn.temps[x] <= tourn.clients[x].t2,range(len(tourn.indices))))) and (tourn.poids.energie <= triporteur.charge))

from itertools import product

def Clarke(triporteurs,graphe,clients,elp,t0 = 8*3600 + 1,requirements = req,ponderation = lambda x: x.energie):
    def dist(a,b):
        if a in graphe:
            if b in graphe[a]:
                return graphe[a][b]
        else:
            return Poids(np.inf,np.inf,False)
        
    n = len(clients) + 1
    nlist = clients.copy()
    nlist.insert(0,elp)
    tri0 = triporteurs[0]
    gains = [(i,j,s(clients,dist,i,j,elp)) for i, j in product(range(1,n-1), range(1,n-1)) if i != j]
    gains.sort(key = lambda x : ponderation(x[2]),reverse = True)# Ce sont les gains potentiels, on adopte une strategie gloutonne en privilegiant les gains les plus gros.
    sw = {}
    ew = {}
    for i in range(1,n-1):
        swi= Tournee(i,elp,dist,clients)
        ewi = Tournee(i,elp,dist,clients)
        if requirements(tri0,swi,t0):
            sw[i] = swi
            ew[i] = ewi
    while True:
        if len(gains) == 0:
            break
        i,j,sij = gains[0]
        if i in ew and j in sw and j != ew[i].indices[0]:#si les tournees existent et sont differentes
            tfus = ew[i] + sw[j]
            if requirements(tri0,tfus,t0):
                merge(clients,i,j,sw,ew)
            else:
                del gains[0]
        else:
            del gains[0]
            
    l = []
    for i in sw.values():
        i.indices.append(0)
        i.indices.insert(0,0)
        two_opt(lambda x,y:ponderation(dist(x,y)),nlist,i.indices)
        l.append((i.indices,i.poids))
    prevus = []    
    l.sort(key = lambda x:ponderation(x[1]),reverse = True)
    for tripo in triporteurs:
        if len(l) == 0:
            break
        else:
            if tripo.liste_tournee == []:
                a_livrer = l[0][0]
                del a_livrer[0]
                del a_livrer[len(a_livrer)-1]
                prevus = prevus + a_livrer
                tourneedutripo = list(map(lambda x:nlist[x],a_livrer))
                tourneedutripo.append(elp)
                tripo.liste_tournee = tourneedutripo
                del l[0]
    def set_diff(l1,l2):
        nl = []
        for i in l1:
            if not (i in l2):
                nl.append(i)
        return(nl)
    clients_indices = set_diff([i for i in range(len(clients))],prevus)
    clients = [clients[i] for i in clients_indices]
    return clients
def cout(dst,tourn):
    d = 0
    for i in range(len(tourn) - 1):
        d = d + dst(tourn[i],tourn[i+1])
    return(d)

def ajout(dst,tourn,dps):
    n = len(tourn)
    k = len(dps)
    route = [i for i in range(n+k)]
    nt = tourn[:n-1] + dps + [tourn[n-1]] #l'elp est a la fin
    ropt = two_opt(dst,nt,route)
    return map(lambda x:tourn[x] if x < n else dps[x],ropt)                      

def ajout_indice(dst,tourn,dp):
    n = len(tourn)
    route = [i for i in range(n+1)]
    nt = tourn[:n-1] + [dp] + [tourn[n-1]] #l'elp est a la fin
    ropt = two_opt(dst,nt,route)
    k = 0
    for i in range(len(ropt)):
        if ropt[i] == n:
            return(i,map(lambda x:tourn[x] if x < n else dp))

def ajout_segm(tourn,dp1,dp2,dst):
    (idp1,to1) = ajout_indice(dst,tourn,dp1)
    (idp2,to2) = ajout_indice(dst,tourn,dp2)
    poss1 = to1[:idp1] + ajout(dst,to1[idp1:],dp2)
    poss2 = ajout(dst,to2[:idp2 + 1],dp1) + to2[idp2 + 1:]
    if cout(dst,poss1) < cout(dst,poss2):
        return(poss1)
    else:
        return(poss2)

def cout_ajout(dst,tour,dp1,dp2):
    return(cout(dst,ajout_segm(tour,dp1,dp2,dst)) - cout(dst,tour))

def nouveau_segment(triporteurs,dp1,dp2,dst = lambda x:x.energie): #Cette fonction vise a rajouter un segment dans la tournee d'un triporteur existant : ()
    cost = []
    n = len(triporteurs)
    for i in range(n):
        tourn = triporteurs[i].tournee
        cost.append(i,cout_ajout(dst,tourn,[dp1,dp2]))
    (m,cm) = cost.min(key = lambda x:x[1])
    triporteurs[m].tournee = ajout_segm(triporteurs[m].tournee,dp1,dp2,dst)

def borne_tournee(dst,triporteur,bornes): #il y a tres peu de bornes
    tourn = triporteur.tournee
    cost = [(i,cout_ajout(dst,tourn,[bornes[i]])) for i in range(len(bornes))]
    i,c = cost.min(key = lambda x:x[1])
    return ajout(dst,tourn,bornes[i])
