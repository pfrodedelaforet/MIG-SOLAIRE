vitessepiet = 10/3.6
vitesse = 25/3.6
from math import sqrt
import random
from collections import defaultdict
from  mig_algo_energie_final import *
from classes import *
from pyproj import Transformer
import time
import networkx as nx

def coor_point(coor):#on transforme dictionnaire de listes de coordonnées en dictionnaire de listes de points.
    return {Point(list(coor.keys())[i][0],list(coor.keys())[i][1]):
            [Point(coor[list(coor.keys())[i]][j][0], coor[list(coor.keys())[i]][j][1]) 
            for j in range(len(coor[list(coor.keys())[i]]))] for i in range(len(list(coor.keys()))) }

def distance_euc(point1, point2):
    return sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2)

#ici, on génère un ensemble aléatoire de stop, à raison d'un tous les 10 m avec une probabilité de 1/5.
def stop(coor_points): 
    tabstop = defaultdict(dict)
    for i in range(len(list(coor_points.keys()))) : 
        p = list(coor_points.keys())[i]
        for j in range(len(coor_points[list(coor_points.keys())[i]])) :
            q = coor_points[list(coor_points.keys())[i]][j] ; tabstop[p][q] = [] 
            for k in range(1,int(distance_euc(list(coor_points.keys())[i],
                            coor_points[list(coor_points.keys())[i]][j])/10)):
                if random.randrange(1, 5) == 1:
                    tabstop[p][q].append(10 *k)
    return tabstop

def grosgraph(coor_points, altitude, velo, usager = 75, puissmax_usager = 250):#ici, on génère grosgraphe
    grosgraphe = defaultdict(dict) ; tabstop = stop(coor_points)
    for i in range(len(list(coor_points.keys()))) : 
        p = list(coor_points.keys())[i]
        grosgraphe[p] = {}
        for j in range(len(coor_points[list(coor_points.keys())[i]])) :
            q = coor_points[list(coor_points.keys())[i]][j]
            if p != q: 
                progarthur = calcul_energy([[distance_euc(p, q), altitude[(p.latitude, p.longitude)], 
                                            altitude[(p.latitude, p.longitude)], vitesse, tabstop[p][q]]], 
                                            velo, usager , puissmax_usager)
                if type(progarthur) != str:
                    grosgraphe[p][q] = progarthur[0] + usager * progarthur[3]*2
                else : 
                    grosgraphe[p][q] = float("inf")
    return (grosgraphe, tabstop)




def get_path_to(dist, node):# programme utile pour djikstrahomemade
    prev = dist[node][1]
    path = [node]
    while prev is not None:
        path.insert(0, prev)
        prev = dist[prev][1]
    return path  

def djikstrahomemade(graphe,depart):
    visites = set()
    nonvisites = set(graphe)
    dist = {k: (np.inf, None) for k in graphe}    
    dist[depart] = (0, None)
    etape = depart 
    nonvisites.remove(etape)
    while len(nonvisites) > 0:
        visites.add(etape)
        for voisin in graphe[etape].keys():
            if voisin in nonvisites:
                new_dist = dist[etape][0] + graphe[etape][voisin]
                if dist[voisin][0]> new_dist:
                    dist[voisin] = (new_dist, etape)
        distance = float('inf')
        x_min = list(nonvisites)[0]
        for x in nonvisites: 
            if (float(dist[x][0])<float(distance)) : 
                x_min = x
                distance = dist[x][0]
        etape = x_min
        nonvisites.remove(etape)
    D = {}
    for fin in graphe : 
        D[fin] = (dist[fin][0], get_path_to(dist, fin))
    return D


def djikstra(graphe, t = None):
    G = nx.DiGraph()
    for p in list(graphe.keys()):
        G.add_node(p)
        G.add_weighted_edges_from([(p,q,graphe[p][q]) for q in graphe[p]])
    return (nx.shortest_path_length(G, t), nx.shortest_path(G, t))
    



def temps(djikdep, p, q, altitude, velo, coor_points, usager = 75, puissmax_usager = 250):
    t = 0.0
    L = djikdep[1][q] #on récup le path entre les deux points
    tabstop = stop(coor_points)
    for i in range(len(L)-1):
        deltat = calcul_energy([[distance_euc(L[i], L[i+1]), altitude[(L[i].latitude, L[i].longitude)], 
                                altitude[(L[i+1].latitude, L[i+1].longitude)], vitesse, tabstop[L[i]][L[i+1]]]],
                                velo, usager, puissmax_usager)[3]
        if deltat == 'i':#trajet impossible
            t += float("inf")
        else:
            print(deltat)
            t += float(deltat)
    return t 




def trouvpoint(grosgraphe_0, depart, arrivee, tdepuisdep, altitude, velo, coor_points, 
                usager = 75, puissmax_usager = 250):
    i = 0 ; dep = Point(depart.latitude, depart.longitude) 
    arr = Point(arrivee.latitude, arrivee.longitude)
    L = djikstra(grosgraphe_0, dep)
    while temps(L, dep, L[1][arr][i], altitude, velo, coor_points, usager, puissmax_usager)< tdepuisdep : 
        i+=1
    return L[1][Point(arrivee.latitude, arrivee.longitude)][i] #c'est de la classe point

def approx(nodeslist, coor_points):
    for i in range(len(nodeslist)) :
        distmin = float("inf") ; cmin = list(coor_points.keys())[0]
        for c in list(coor_points.keys()) : 
            if distance_euc(c, nodeslist[i])<distmin:
                distmin = distance_euc(c, nodeslist[i])
                cmin = c
        nodeslist[i].latitude = cmin.latitude
        nodeslist[i].longitude = cmin.longitude
    return nodeslist

def graph(coor_points, altitude, nodeslist, bornes, velo, usager = 75, puissmax_usager = 250):
    sousgraphe = defaultdict(dict)
    liste = approx(nodeslist + bornes, coor_points)
    liste_ = [Point(elt.latitude, elt.longitude) for elt in liste]
    grosgraphe = grosgraph(coor_points, altitude, velo, usager, puissmax_usager)[0] 
    for p in liste_:
        ener_p = djikstra(grosgraphe, p)
        for q in liste_:
            ener_pq = ener_p[0][q] 
            if (p != q and ener_pq != float("inf")):
                sousgraphe[p][q] = Poids(ener_pq, temps(ener_p, p, q, altitude, velo,
                                        coor_points,usager, puissmax_usager),True)                
            else:
                sousgraphe[p][q] = Poids(float('inf'), float('inf'), False)
    return sousgraphe
#attention les bornes et les points de livraison sont seulement des points ici, pour 
# les différencier il faut avoir la liste des bornes                                 


