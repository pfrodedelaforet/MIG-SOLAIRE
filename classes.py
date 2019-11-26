from pyproj import Transformer



class Point :
    transformer_to_lamb = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
    transformer_to_lat_long = Transformer.from_crs( "EPSG:2154","EPSG:4326", always_xy=True)
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
        self.x = Point.transformer_to_lamb.transform(lat,lon)[0]
        self.y = Point.transformer_to_lamb.transform(lat,lon)[1]
        #self.alti = cartalt[round((self.x-xo) / pas)][round((self.y-yo) / pas)]
    
    def __repr__(self) :
        return (f"point de latitude {self.latitude}, de longitude {self.longitude}, d'altitude {self.alti}, x={self.x}, y={self.y} ")
    
    def __eq__(self, other):
        return ((self.latitude == other.latitude) and (self.longitude == other.longitude))

class DeliveryPoint(Point):
    def __init__(self, lat, lon, t1, t2,masse):
        Point.__init__(self, lat, lon)
        self.t1 = t1
        self.t2 = t2
        self.masse = masse #masse du colis a livrer en kg
    def __repr__(self):
        return (Point.__repr__(self)+f"il veut être livré entre {self.t1} et {self.t2}")
    
    def __eq__(self, other):
        return ((self.latitude, self.longitude, self.t1, self.t2, self.masse)==(other.latitude, other.longitude, other.t1, oter.t2, other.masse))


class Triporteur:
    def __init__(self, capacity, charge, elp, v,puissance_batterie,puissance_moteur,batterie_capacity):
        self.capacity = capacity #flottant : poids qu'il peut porter
        self.charge = charge #flottant : charge du triporteur : en w.h
        self.pos = [elp.x,elp.y]
        self.liste_tournee = [] #Liste de DeliveryPoint
        self.last_dv_point = elp #de type point : elp de départ du triporteur
        self.vitesse = v #en m/s 
        self.taille_arrete = -1
        self.prop_arrete = 0
        self.puissance_batterie=puissance_batterie
        self.puissance_moteur=puissance_moteur
        self.batterie_capacity=batterie_capacity
        self.time_to_be_fully_charged=(batterie_capacity-charge)/puissance_batterie
        xy = convert(self.pos[0],self.pos[1],echelles)
        self.dot = plt.scatter(xy[0],xy[1],s=100)
    def avancer(self,dist,t):
        if self.taille_arrete == -1 and self.liste_tournee != []:
            self.taille_arrete = dist[self.last_dv_point,self.liste_tournee[0]] 
        proptot = self.vitesse*t/self.taille_arrete + self.prop_arrete
        if proptot < 1:
            self.prop_arrete = proptop
            self.pos = [self.last_dv_point.x + (self.liste_tournee[0].x-self.last_dv_point.x)*self.prop_arrete,self.last_dv_point.y + (self.liste_tournee[0].y-self.last_dv_point.y)*self.prop_arrete]
        else:
            self.last_dv_point = self.liste_tournee[0]
            self.pos = [last_dv_point.x,last_dv_point.y]
            del self.tournee[0]
            reste = (proptop-1)*self.taille_arrete/self.vitesse
            self.taille_arrete = -1
            self.prop_arrete = 0
            self.avancer(dist,reste) 
        
    def __repr__(self):
        str(self.capacity,self.dispo,self.position, self.charge)
"""class Bornes(Point):
    def __init__(self, lat, lon, priseslibres, charges):
        Point.__init__(self, lat, lon)
        self.priseslibres = priseslibres #tableau de booleen: à chaque case du tableau est associée une prise
        self.charges = charges #tableau en Wh des charges de chacune des batteries 
    def reserv(self):
        for i in range(len(priseslibres)):
            if priseslibres[i] & :# ajouter condition de choix fixée par romain et Jeremy
                priseslibres[i] = False #on choisit la prise 
                return i
        return None #ie c'est tout réservé déjà
    def dereserv(self, i, chargetriporteuravant):
        priseslibres[i] = True 
        charges[i] = chargetriporteuravant #ie on a remplacé la batterie par la notre          
""" 
class Poids:
    def __init__(self, energienecess, t, faisable):
        self.energie = energienecess
        self.duree = t
        self.faisable = faisable #un booléen 
    def __add__(self,other): #Commutatif
        return Poids(self.energie+other.energie,self.duree + other.duree, self.faisable and other.faisable)
    
    def __sub__(self,other):
        return Poids(self.energie-other.energie,self.duree - other.duree, self.faisable)

#C'est pour le programme de Jeremy    
def _tourns(clients,dist,i,j,elp): #C'est un Poids ,s permet l'optimisation des tournees c'est une matrice len(pts)� ,i et j sont des indices, clients une liste de DeliveryPoint
    return(dist(clients[i],elp) + dist(elp,clients[j]) - dist(clients[i],clients[j]))

class Tournee:
    def __init__(self,i0,elp,dist,clients):#i0 est un indice, elp un point et dist une fonction de la forme i -> j -> poids ou i et j sont des points, clients est une liste de DeliveryPoint
        self.poids = Poids(dist(elp,clients[i0]) + dist(clients[i0],elp))
        self.elp = elp
        self.indices = [i0] #il est implicite qu'une tournee commence et finit par l'elp, il faut prendre cela en compte, les points sont un couple DeliveryPoint, heure d'arrivee presumee(en secondes, on suppose qu'on est a l'elp a t = 0)
        self.temps = [dist(elp,clients[i0].duree]
        self.clients = clients
        self.dist = dist
        self.masse = clients[i0].masse
    
    def __add__(self,other):#Pas du tout commutatif
        tmp = tournee(self.indices[0],self.elp,self.dist,self.clients)
        ttourn1 = self.temps[-1]
        ot = other.temps.copy()
        elp = self.elp
        i = self.indices[-1]
        ti = self.temps[-1]
        j = other.indices[0]
        clients = self.clients
        for k in range(len(ot)): #il faut changer le moment de passage de la deuxieme tournee
            ot[k] += dist(clients[i],clients[j]).duree + ti - dist(elp,clients[j]).duree
            
        tmp.temps = self.indices + ot
        tmp.poids = self.poids + other.poids - _tourns(self.clients,self.dist,self.indices[-1],other.indices[0])
        tmp.masse = self.masse + other.masse
        return(tmp)
