
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
    def __init__(self, capacity, dispo, point, charge):
        self.capacity = capacity #flottant : poids qu'il peut porter
        self.dispo = dispo #booleen : le triporteur est pret a partir
        self.charge = charge #flottant : charge du triporteur : en w.h
        self.point = point #point
        self.charge = charge #en %
    def __repr__(self):
        str(self.capacity,self.dispo,self.position, self.charge)
           
 
