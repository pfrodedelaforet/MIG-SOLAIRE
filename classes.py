class Triporteur:
    def __init__(self,capacity,dispo,position):
        self.capacity = capacity #flottant : poids qu'il peut porter
        self.dispo = dispo #booleen : le triporteur est prêt à partir
        self.position = position #point
    def __repr__(self):
        str(self.capacity,self.dispo,self.position)
