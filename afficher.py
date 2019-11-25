import time
from conversion import conversion
import numpy as np
import matplotlib.pyplot as plt
import math
from creer_liste_clients import creer_clients_csv
from maptograph import graph
from classes import *
from pyproj import Transformer
from optimisation_des_tournees import Clarke
from mig_algo_energie_final import Velo

from urllib.request import Request, urlopen
from io import BytesIO
from PIL import Image
#transformer_to_lamb = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
#transformer_to_lat_long = Transformer.from_crs( "EPSG:2154","EPSG:4326", always_xy=True)



def init_carte():
    """carte : image png du cadre de l'algorithme
       bords : [x1,y1,x2,y2] les bords du rectangle"""
    def deg2num(lat_deg, lon_deg, zoom):
      lat_rad = math.radians(lat_deg)
      n = 2.0 ** zoom
      xtile = int((lon_deg + 180.0) / 360.0 * n)
      ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
      return (xtile, ytile)

    def num2deg(xtile, ytile, zoom):
      n = 2.0 ** zoom
      lon_deg = xtile / n * 360.0 - 180.0
      lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
      lat_deg = math.degrees(lat_rad)
      return (lat_deg, lon_deg)



    def getImageCluster(lat_deg, lon_deg, delta_lat,  delta_long, zoom):
        smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
        xmin, ymax =deg2num(lat_deg, lon_deg, zoom)
        xmax, ymin =deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)

        Cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) ) 
        for xtile in range(xmin, xmax+1):
            for ytile in range(ymin,  ymax+1):
                imgurl=smurl.format(zoom, xtile, ytile)
                req = Request(imgurl, headers={'User-Agent': "AppleWebKit/537.36"})
                print("Opening: " + imgurl)
                imgstr = urlopen(req).read()
                tile = Image.open(BytesIO(imgstr))
                Cluster.paste(tile, box=((xtile-xmin)*256 ,  (ytile-ymin)*255))

        return (Cluster,xmin,xmax,ymin,ymax)


    lat = 43.69795
    longi = 7.26763
    a = getImageCluster(lat,longi, 0.00746,0.0251, 16)
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    tab = np.asarray(a[0])
    plt.imshow(tab)
    echelles = [a[1],a[2],a[3],a[4],len(tab),len(tab[0])]

def actualiser_carte(liste_tripo): 
    """liste_tripo : liste d'objets de type triporteur"""
    for elt in liste_tripo:
        elt.dot.set_offset(self.pos[0],self.pos[1])

def dicos():
    list_coor=np.genfromtxt('liste_coordonees.csv',delimiter=',')
    list_route=np.genfromtxt('liste_adjacence.csv',delimiter=',')
    dico_points={}
    for i,point in enumerate(list_coor):
        dico_points[(point[0],point[1])] = [(list_coor[int(j)][0],list_coor[int(j)][1]) for j in list_route[i] if not np.isnan(j)]
    def route(i,j):
        if j in dico_points[i]:
            return 1
        else:
            return 0
    altitude_route=np.genfromtxt('altitude_route.csv',delimiter=',')
    altitude={}
    for i,point in enumerate(list_coor):
        altitude[(point[0],point[1])] = altitude_route[i]
    
    return dico_points, altitude

def boucle(n,v,nb_clients,t,capacity,charge,elp):
    """n : nombre de triporteurs
       clients : liste d'objets de classe delivery_point
       dist : dist[i][j] renvoit la distance entre i et j"""

    bornes = []
    liste_clients = creer_clients_csv(nb_clients,csv = "shops.csv")

    dico_points,altitude = dicos()
    dist = graph(dico_points,altitude,liste_clients,bornes,elp,Velo(400))

    liste_tripo = [Triporteur(capacity, charge, elp,v) for i in range(n)]

    init_carte()
    while 1:
        print("boucle")
        Clarke(liste_tripo,dist,liste_clients,elp)
        for elt in liste_tripo:
            if elt.liste_tournee != []:
                elt.avancer(dist,t)
            actualiser_carte(liste_tripo)
        time.sleep(t)
nb_clients = 30
elp = Point(43.707354, 7.282234)
boucle(5,1,nb_clients,1,100,1000,elp)
plt.show()

