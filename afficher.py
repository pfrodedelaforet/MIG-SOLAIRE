import time
import numpy as np
import matplotlib.pyplot as plt
import math

from urllib.request import Request, urlopen
from io import BytesIO
from PIL import Image



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


    a = getImageCluster(43.69795,7.26763, 0.00746,0.0251, 16)
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    tab = np.asarray(a[0])
    plt.imshow(tab)
    echelles = [a[1],a[2],a[3],a[4],len(tab),len(tab[0])]

def actualiser_carte(liste_tripo): 
       """liste_tripo : liste d'objets de type triporteur"""
    for elt in liste_tripo:
        elt.dot.set_offset(self.pos[0],self.pos[1])

def boucle(n,v,liste_clients,t,capacity,charge,elp):
    """n : nombre de triporteurs
       clients : liste d'objets de classe delivery_point
       dist : dist[i][j] renvoit la distance entre i et j"""
    dist = pierre_balance(elp,liste_clients)
    liste_tripo = [Triporteur(capacity, charge, elp,v) for i in range(n)]
    init_carte()
    while 1:
        algorithme(n,liste_tripo,dist,liste_clients)
        for elt in liste_tripo:
            if elt.liste_tournee != []:
                elt.avancer(dist,t)
            actualiser_carte(liste_tripo)
        time.sleep(t)

boucle(5,1,liste_clients,1,100,1000,elp)
