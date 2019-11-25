#on recupere la carte sous forme de dictionnaire dont la clé est un identifiant de point et coor[id] renvoie la liste des coordonnées des points auxquel id est relié
#Elle envoie aussi une fonction  
#Arthur m'envoie ensuite le programme qui prend une suite de quintuplets et qui renvoie la dépense énergétique et la puissance maximale. 
#elle devrait aussi m'envoyer la liste des Booléens tq piet[i][j] = 1 si il y a une zone piétonne 0 sinon 
vitessepiet = 10/3.6
vitesse = 25/3.6
from math import sqrt
import random

def distance_euc(L, N):
    return sqrt((L[0]-N[0])**2+(L[1]-N[1])**2)


def speed(piet, i, j):
    if piet[i][j] == 1:
        return vitessepiet
    else :
        return vitesse

def stop(coor):
    tabstop = {}
    for i in range(len(coor.keys())) : 
        p = Point(coor.keys()[i][0],coor.keys()[i][1]);tabstop[p] = {}
        for j in range(len(coor[i])) :
            q = Point(coor[coor.keys()[i]][j][0],coor[coor.keys()[i]][j][1]) ; tabstop[p][q] = [] 
            for k in range(int(distance_euc(coor.keys()[i],coor[coor.keys()[i]][j])/10)):
                if random.randrange(1, 5) == 1:
                    tabstop[p][q].append(10 *k) #les 3 dernières lignes c'est la génération de la matrice stop aléatoirement
    return tabstop

def grosgraph(coor, altitude, velo, usager = 75, puissmax_usager = 250):
    grosgraphe = {}
    for i in range(len(coor.keys())) : 
        p = Point(coor.keys()[i][0],coor.keys()[i][1])
        grosgraphe[p] = {}
        for j in range(len(coor[i])) :
            q = Point(coor[coor.keys()[i]][j][0],coor[coor.keys()[i]][j][1])
            progarthur = calcul_energy([(distance_euc(coor.keys()[i],coor[coor.keys()[i]][j]), altitude[(coor.keys()[i][0], coor.keys()[i][1])], altitude[(coor[coor.keys()[i]][j][0], coor[coor.keys()[i]][j][1])], vitesse, stop(coor)[p][q])], velo, usager = 75, puissmax_usager = 250)
            grosgraphe[p][q] = progarthur[0] + puisempl * distance_euc(coor[i],coor[j])/progarthur[2]
    return grosgraphe
                
def graphvit(coor, altitude, velo, usager = 75, puissmax_usager = 250):
    graphvit = {}
    for i in range(len(coor.keys())) : 
        p = Point(coor.keys()[i][0],coor.keys()[i][1])
        graphvit[p] = {}
        for j in range(len(coor[i])) :
            stop = []
            for k in range(int(distance_euc(coor.keys()[i],coor[coor.keys()[i]][j])/10)):
                if random.randrange(1, 5) == 1:
                    stop.append(10 *k) #les 3 dernières lignes c'est la génération de la matrice stop aléatoirement
            q = Point(coor[coor.keys()[i]][j][0],coor[coor.keys()[i]][j][1])
            progarthur = calcul_energy((distance_euc(coor.keys()[i],coor[coor.keys()[i]][j]), altitude[(coor.keys()[i][0], coor.keys()[i][1])], altitude[(coor[coor.keys()[i]][j][0], coor[coor.keys()[i]][j][1])], vitesse, []))
            graphvit[p][q] = progarthur[2]
    return graphvit #graphvit est un graphe de point donnant la vitesse entre pointi et pointj si pointi et pointj sont adjacents


def recurs(graphe, x, s, t, P):
    M={}
    if P[x] == s:
        M.append(s)
        M.reverse()
        return M
    if P[x] != s :
        M.append(P[x])
        return recurs(graphe, P[x], M, s, t, P)
        

def djikstra(graphe,etape,fin,visites,dist,P,depart):
    if etape == fin : 
        return (dist[fin], recurs(graphe, fin, depart, fin, P))
    if len(visites) == 0:
        dist[etape] = 0
    for voisin in graphe[etape].keys():
        if voisin not in visites:
            if dist[voisin]>dist[etape] + graphe[etape][voisin]:
                dist[voisin] = dist[etape]+graphe[etape][voisin]
                P[voisin] = etape
    visites.append(etape)
    distance = float('inf')
    for x in graphe.keys():
        if x not in visites : 
            if dist[x]<distance : 
                x_min = x
                distance = dist[x]
    return djikstra(graphe, x_min, fin, visites, dist, P, depart)
    

def path_clients(coor, altitude, nodeslist, bornes, elp, velo, usager = 75, puissmax_usager = 250):#nodeslist et bornes sont des listes de point
    M = {}
    for s in nodeslist.union(bornes.union(elp)):
        M[s] = {}
        for t in nodeslist.union(bornes.union(elp)):
            M[s][t] = djikstra(grosgraph(coor, altitude, velo, usager = 75, puissmax_usager = 250), s, t, [], graph[s], {}, s)[1]
    return M #ca renvoie un graphe de liste avec les listes de point liant les point du graphe


def temps(coor, altitude, depart, arrivee, velo, usager = 75, puissmax_usager = 250):
    t = 0; L = djikstra(grosgraph(coor, altitude, velo, usager = 75, puissmax_usager = 250), depart, arrivee, [], graph[depart], {}, depart)[1] ; graphvitesse = graphvit(coor, velo, usager = 75, puissmax_usager = 250)
    for i in range(len(L)-1):
        t += distance_euc(L[i],L[i+1])/graphvitesse[L[i]][L[i+1]]
    return t 


def trouvpoint(coor, altitude, depart, arrivee, tdepuisdep):
    i = 0 ; L = djikstra(grosgraph(coor, altitude, velo, usager = 75, puissmax_usager = 250), depart, arrivee, [], graph[depart], {}, depart)[1]
    while temps(coor, altitude, depart, L[i], velo, usager = 75, puissmax_usager = 250)< tdepuisdep : 
        i+=1
    return L[i] #c'est de la classe point



def graph(coor, altitude, nodeslist, bornes, elp, velo, usager = 75, puissmax_usager = 250):
    sousgraphe = {}
    for s in nodeslist.union(bornes.union(elp)) : 
        sousgraphe[s] = {} 
        for t in nodeslist.union(bornes.union(elp)) : 
            progarthur = calcul_energy([(distance_euc((s.latitude,s.longitude),(t.latitude, t.longitude)), altitude[(s.latitude, s.longitude)], altitude[(t.latitude, t.longitude)], vitesse, stop)], velo, usager = 75, puissmax_usager = 250)
            if type(progarthur != str ): 
                sousgraphe[s][t] = Poids(djikstra(grosgraph(coor, altitude, velo, usager = 75, puissmax_usager = 250), s, t, [], graph[s], {}, s)[0], temps(coor, s, t),True)
    return sousgraphe
#attention les bornes et les points de livraison sont seulement des points ici, pour les différencier il faut avoir la liste des bornes                                 
