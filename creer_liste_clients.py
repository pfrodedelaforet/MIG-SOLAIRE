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
    csample = clients.sample(nb_clients)
    csample['poids'] = ci(rd.sample(len(csample['osm_id']))) 
    csample['horaires'] = np.full(len(csample['osm_id']),horaire[0])
    csample['delivery_point'] = tdp(csample['lat'],csample['lon'],np.full(len(csample['osm_id']),horaire[0]),np.full(len(csample['osm_id']),horaire[1]),csample['poids'])
    dps = csample['delivery_point']
    cl = []
    for i in dps:
        cl.append(i)
    return(cl)
