
class Point :
    def __init__(self, lat, lon) :
        self.latitude = lat
        self.longitude = lon
        self.id = router.findNode(lat, lon)
        self.x = transformer_to_lamb.transform(lat,lon)[0]
        self.y = transformer_to_lamb.transform(lat,lon)[1]
        self.alti = cartalt[round((self.x-xo) / pas)][round((self.y-yo) / pas)]
    
    def __repr__(self) :
        return (f"point de latitude {self.latitude}, de longitude {self.longitude}, d'altitude {self.alti}, x={self.x}, y={self.y} ")
class DeliveryPoint(Point):
    def __init__(self, lat, lon, t1, t2):
        Point.__init__(self, lat, lon)
        self.t1 = t1
        self.t2 = t2
    def __repr__(self):
        return (Point.__repr__(self)+f"il veut être livré entre {self.t1} et {self.t2}")
class Triporteur:
    def __init__(self, capacity, dispo, point, charge, elp):
        self.capacity = capacity #flottant : poids qu'il peut porter
        self.dispo = dispo #booleen : le triporteur est pret a partir
        self.charge = charge #flottant : charge du triporteur : en w.h
        self.point = point #point
        self.charge = charge #en %
        self.liste_tournee = []
    #Zone Tristan je vous aime
        self.last_dv_point = elp #de type point : elp de départ du triporteur
        self.vitesse = 5 #en m/s 
        self.taille_arrete = -1
        self.prop_arrete = 0

    def avancer(self,dist,t):
        if self.taille_arrete == -1:
            self.taille_arrete = dist[self.last_dv_point,self.liste_tournee[0]] 
        proptot = self.vitesse*t/self.taille_arrete + self.prop_arrete
        if proptot < 1:
            self.prop_arrete = proptop
            #à deplacer 
        else:
            self.last_dv_point = self.liste_tournee[0]
            del self.tournee[0]
            reste = (proptop-1)*self.taille_arrete/self.vitesse
            self.taille_arrete = -1
            self.prop_arrete = 0
            self.avancer(dist,reste) 
        


    def __repr__(self):
        str(self.capacity,self.dispo,self.position, self.charge)
 class Bornes(Point):
    def __init__(self, lat, lon, priseslibres, charges):
        Point.__init__(self, lat, lon)
        self.priseslibres = priseslibres #tableau de booleen: à chaque case du tableau est associée une prise
        self.charges = charges #tableau en Wh des charges de chacune des batteries 
    def reserv(self):
        for i in range len(priseslibres):
            if priseslibres[i] & :# ajouter condition de choix fixée par romain et Jeremy
                priseslibres[i] = False #on choisit la prise 
                return i
        return None #ie c'est tout réservé déjà
    def dereserv(self, i, chargetriporteuravant):
        priseslibres[i] = True 
        charges[i] = chargetriporteuravant #ie on a remplacé la batterie par la notre          
 
class Poids:
    def __init__(self, energienecess, t, faisable):
        self.energie = energienecess
        self.duree = t
        self.faisable = faisable #un booléen 