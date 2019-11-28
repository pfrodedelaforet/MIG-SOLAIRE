#on recupere la carte sous forme de dictionnaire dont la clé est un identifiant de point et coor[id] renvoie la liste des coordonnées des points auxquel id est relié
#Elle envoie aussi une fonction  
#Arthur m'envoie ensuite le programme qui prend une suite de quintuplets et qui renvoie la dépense énergétique et la puissance maximale. 
#elle devrait aussi m'envoyer la liste des Booléens tq piet[i][j] = 1 si il y a une zone piétonne 0 sinon 
vitessepiet = 10/3.6
vitesse = 25/3.6
from math import sqrt
import random
from collections import defaultdict
from  mig_algo_energie_final import *
from classes import *
from pyproj import Transformer
transformer_to_lamb = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
transformer_to_lat_long = Transformer.from_crs( "EPSG:2154","EPSG:4326", always_xy=True)
import time
import networkx as nx
def coor_point(coor):
    return {Point(list(coor.keys())[i][0],list(coor.keys())[i][1]):[Point(coor[list(coor.keys())[i]][j][0], coor[list(coor.keys())[i]][j][1]) for j in range(len(coor[list(coor.keys())[i]]))] for i in range(len(list(coor.keys()))) }
def distance_euc(point1, point2):
    return sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2)

def speed(piet, i, j):
    if piet[i][j] == 1:
        return vitessepiet
    else :
        return vitesse

def stop(coor_points):
    tabstop = defaultdict(dict)
    for i in range(len(list(coor_points.keys()))) : 
        p = list(coor_points.keys())[i]
        for j in range(len(coor_points[list(coor_points.keys())[i]])) :
            q = coor_points[list(coor_points.keys())[i]][j] ; tabstop[p][q] = [] 
            for k in range(1,int(distance_euc(list(coor_points.keys())[i],coor_points[list(coor_points.keys())[i]][j])/10)):
                if random.randrange(1, 5) == 1:
                    tabstop[p][q].append(10 *k)
    return tabstop

def grosgraph(coor_points, altitude, velo, usager = 75, puissmax_usager = 250):
    grosgraphe = defaultdict(dict) ; tabstop = stop(coor_points)
    for i in range(len(list(coor_points.keys()))) : 
        p = list(coor_points.keys())[i]
        grosgraphe[p] = {}
        for j in range(len(coor_points[list(coor_points.keys())[i]])) :
            q = coor_points[list(coor_points.keys())[i]][j]
            if p != q: 
                progarthur = calcul_energy([[distance_euc(p, q), altitude[(p.latitude, p.longitude)], altitude[(p.latitude, p.longitude)], vitesse, tabstop[p][q]]], velo, usager , puissmax_usager)
                if type(progarthur) != str:
                    grosgraphe[p][q] = progarthur[0] + usager * progarthur[3]*2
                else : 
                    grosgraphe[p][q] = float("inf")
    return (grosgraphe, tabstop)
                
def graphvit(coor_points, altitude, velo, usager = 75, puissmax_usager = 250):
    graphvit = {} ; tabstop = stop(coor_points)
    for i in range(len(list(coor_points.keys()))) : 
        p = list(coor_points.keys())[i]
        graphvit[p] = {}
        for j in range(len(coor_points[list(coor_points.keys())[i]])) :
            q = coor_points[list(coor_points.keys())[i]][j]
            if p!=q:
                progarthur = calcul_energy([[distance_euc(p, q), altitude[(p.latitude, p.longitude)], altitude[(p.latitude, p.longitude)], vitesse, tabstop[p][q]]], velo, usager , puissmax_usager)
                if type(progarthur) != str:
                    graphvit[p][q] = progarthur[2]
    return graphvit #graphvit est un graphe de point donnant la vitesse entre pointi et pointj si pointi et pointj sont adjacents






def get_path_to(dist, node):
    prev = dist[node][1]
    path = [node]
    while prev is not None:
        path.insert(0, prev)
        prev = dist[prev][1]
    return path  
def inserer(x, L, dist):#L est une liste déjà triée auparavant 
    i = 0
    for i in range(len(L)):
        if dist[x][0]<dist[L[i]][0]:
            L.insert(i, x)
            return L
def djigstra(graphe,depart):
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


def djikstra(graphe, p):
    G = nx.DiGraph()
    for p in graphe:
        G.add_node(p)
        G.add_weighted_edges_from([(p,q,graphe[p][q]) for q in graphe[p]])
    return (nx.shortest_path_length(G, p), nx.shortest_path(G, p))
    


def path_clients(grosgraphe_0):#nodeslist et bornes sont des listes de point
    M = defaultdict(dict)
    for p in nodeslist+bornes+[elp]:
        M[p] = {}
        plus_court_p = djikstra(grosgraphe_0, p)[1]
        for q in nodeslist+bornes+[elp]:
            M[p][q] = plus_court_p[q]
    return M #ca renvoie un graphe de liste avec les listes de point liant les point du graphe

 




def temps(grosgraphe_0, p, q, altitude, velo, coor_points, usager = 75, puissmax_usager = 250):
    t = 0.0
    L = djikstra(grosgraphe_0, p)[1][q] #on récup le path entre les deux points
    tabstop = stop(coor_points)
    for i in range(len(L)-1):
        deltat = calcul_energy([[distance_euc(L[i], L[i+1]), altitude[(L[i].latitude, L[i].longitude)], altitude[(L[i+1].latitude, L[i+1].longitude)], vitesse, tabstop[L[i]][L[i+1]]]], velo, usager, puissmax_usager)[3]
        if deltat == 'i':
            t = float('inf')
            return t 
        print(deltat)
        t += float(deltat)
    return t 




def trouvpoint(grosgraphe_0, depart, arrivee, tdepuisdep, altitude, velo, coor_points, usager = 75, puissmax_usager = 250):
    i = 0
    L = djikstra(grosgraphe_0, depart)[1][arrivee]
    while temps(grosgraphe_0, depart, L[i], altitude, velo, coor_points, usager, puissmax_usager, )< tdepuisdep : 
        i+=1
    return L[i] #c'est de la classe point

def approx(nodeslist, coor_points):
    for i in range(len(nodeslist)) :
        distmin = float("inf") ; cmin = list(coor_points.keys())[0]
        for c in list(coor_points.keys()) : 
            if distance_euc(c, nodeslist[i])<distmin:
                distmin = distance_euc(c, nodeslist[i])
                cmin = c
        nodeslist[i] = cmin
    return nodeslist


def graph(coor_points, altitude, nodeslist, bornes, elp, velo, usager = 75, puissmax_usager = 250):
    sousgraphe = defaultdict(dict)
    liste = approx(nodeslist + bornes + [elp], coor_points) #bien une liste de points
    grosgraphe = grosgraph(coor_points, altitude, velo, usager, puissmax_usager)[0] ; i= 0
    for p in liste:
        ener_p =  djikstra(grosgraphe, p)[0]
        for q in liste:
            ener_pq = ener_p[q] 
            if (p != q and ener_pq != float("inf") and type(ener_pq) != float):
                sousgraphe[p][q] = Poids(ener_pq, temps(grosgraphe, p, q, altitude, velo,  coor_points,usager, puissmax_usager),True)                
    return sousgraphe
#attention les bornes et les points de livraison sont seulement des points ici, pour les différencier il faut avoir la liste des bornes                                 
