import pandas as pd
import numpy as np
import numpy.random as rd
from classes import *

poids_min = 0.5 #je suppose que les colis vont de 0.5 a 3 kilogrammes
poids_max = 3

def change_int(r):
    return(r*(poids_max-poids_min) + poids_min)

ci = np.vectorize(change_int)

def to_delivery_point(lat,lon,t1,t2,poids):
    return DeliveryPoint(lat,lon,t1,t2,poids)

tdp = np.vectorize(to_delivery_point)
        
def creer_clients_csv(nb_clients,csv="shops.csv",horaire = (8*3600,18*3600)):
    clients = pd.read_csv(csv)
    clients['poids'] = ci(rd.sample(len(clients['osm_id']))) 
    clients['horaires'] = np.full(len(clients['osm_id']),horaire[0])
    clients['delivery_point'] = tdp(clients['lat'],clients['lon'],np.full(len(clients['osm_id']),horaire[0]),np.full(len(clients['osm_id']),horaire[1]),clients['poids'])
    dps = clients['delivery_point']
    return(rd.choice(dps,nb_clients,replace=False))
    
