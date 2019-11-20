class Triporteur:
    def __init__(self,capacity,dispo,position):
        self.capacity = capacity #flottant : poids qu'il peut porter
        self.dispo = dispo #booleen : le triporteur est prêt à partir
        self.position = position #point
    def __repr__(self):
        str(self.capacity,self.dispo,self.position)
        
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
