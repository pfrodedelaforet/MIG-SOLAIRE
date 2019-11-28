crr=0.00962
usager=75
rap=2
from math import *
import numpy as np


class Segment:
    def __init__(self,Velo,alt_dep,alt_fin,l,Lieu,dem): # depart, fin, altitudes et l calculés précedemment stops estimés ou choisis de manièere probabiliste par une fonction auxiliaire départ et fin à ajouter selon le type de données
        self.Velo=Velo #type Velo
        self.l=l #entier
        self.Lieu=Lieu #type Lieu
        self.pente=max(np.arcsin((alt_fin-alt_dep)/l),0) #flottant (en radian)
        d_loc=l-self.Lieu.d_acc#distance en régime établit
        if dem==True:
            if l<self.Velo.d_dem:
                self.pui_rap_max=max((1/rap)*(self.Velo.m*l*self.Velo.a_dem+self.Velo.m*9.81*l*sin(self.pente)/sqrt(2*l/self.Velo.a_dem))-usager,0)
                ene=max((1/rap)*(self.Velo.m*l*self.Velo.a_dem+self.Velo.m*9.81*l*sin(self.pente))-usager*sqrt(2*l/self.Velo.a_dem),0)
                self.ene_wh_rap=(ene/3600)
                self.time=sqrt(2*l/self.Velo.a_dem)
            elif l>=self.Velo.d_dem and l<(self.Lieu.d_acc-self.Velo.d_dem):
                self.pui_rap_max=max((1/rap)*(0.5*self.Velo.m*(self.Velo.a_dem**2)*self.Velo.t_dem+self.Velo.m*9.81*self.Velo.d_dem*sin(self.pente)/self.Velo.t_dem)-usager,0) #la puissance max est celle où on accélère le plus donc la phase 1 (pas aussi évident après car on néglige frottements)
                ene=max((1/rap)*(self.Velo.m*l*self.Velo.a_dem+self.Velo.m*9.81*l*sin(self.pente))-usager*self.Lieu.t_acc,0) #c'est très lourd de faire ene_suite donc on surrestime
                self.ene_wh_rap=(ene/3600)
                self.time=self.Velo.t_dem+sqrt(2*l/self.Velo.a_suite)
            else:

                self.pui_rap=max((1/rap)*((0.5*self.Velo.A*1.2*(self.Lieu.v)**3+(9.81*self.Velo.m*(self.Lieu.crr*cos(self.pente)+sin(self.pente))))*self.Lieu.v)-usager,0)#puissance en vitesse de pointe
                self.pui_dem_rap=max((1/rap)*((0.5*self.Velo.m*(self.Velo.a_dem**2)*self.Velo.t_dem+9.81*self.Velo.m*self.Velo.d_dem*sin(self.pente)/(self.Velo.t_dem)))-usager,0)#puissance demarrage phase 1, la phase 2 demande forcement moins de puissance: même pente et on accélère moins vite
                self.pui_rap_max=max(self.pui_dem_rap,self.pui_rap,0)#max des 2 puissances
                ene_dem=max((1/rap)*(0.5*self.Velo.m*((self.Velo.a_dem*self.Velo.t_dem)**2)+self.Velo.m*9.81*sin(self.pente)*((self.Velo.a_dem*self.Velo.t_dem**2)/2)+0.5*self.Velo.m*((self.Lieu.v)**2-(self.Velo.a_dem*self.Velo.t_dem)**2)+9.81*self.Velo.m*sin(self.pente)*(self.Velo.a_suite*((self.Lieu.t_acc-self.Velo.t_dem)**2)/2)+self.Velo.t_dem*self.Velo.a_dem*(self.Lieu.t_acc-self.Velo.t_dem)-self.Velo.a_dem*0.5*((self.Velo.t_dem)**2))-usager*self.Velo.t_dem-usager*(self.Lieu.t_acc-self.Velo.t_dem),0)#energie demarrage
                ene_suite=self.pui_rap*(d_loc/self.Lieu.v)#energie en vitesse de pointe
                self.ene_wh_rap=((ene_suite+ene_dem)/3600)
                self.time=self.Lieu.t_acc+d_loc/self.Lieu.v
        else:
            self.pui_rap_max=self.pui_rap=max((1/rap)*(0.5*self.Velo.A*1.2*(self.Lieu.v)**3+(9.81*self.Velo.m*(self.Lieu.crr*cos(self.pente)+sin(self.pente)))*self.Lieu.v)-usager,0)
            ene_suite=self.pui_rap*l/self.Lieu.v
            self.ene_wh_rap=(ene_suite/3600)
            self.time=d_loc/self.Lieu.v
    def __repr__(self):
        return f"{self.ene_wh_rap},{self.pui_rap},{self.pui_rap_max}"

class Velo:
    def __init__(self,m,A=0.8,puiss_max=290,rap=2,a_dem=2,a_suite=4/3,t_dem=0.5): #m masse (charge comprise) a_dem est estimé a_suite aussi t_dem aussi (précisables),puissance max
        self.m=m
        self.a_dem=a_dem
        self.a_suite=a_suite
        self.A=A
        self.t_dem=t_dem
        self.d_dem=0.5*a_dem*((t_dem)**2)
        self.rap=rap #rapport de transmission (considéré unique)
        self.puiss_max=puiss_max

class Lieu:
    def __init__(self,v,Velo,crr=0.00962): #vitesse v imposé (estimation), crr dépend de v (doc), t_acc estimé
        self.v=v #flottant
        self.crr=crr #flottant
        self.Velo=Velo #type Velo
        self.t_acc=(v-self.Velo.a_dem*self.Velo.t_dem)/self.Velo.a_suite+self.Velo.t_dem+0.5 #flottant gonflé un peu
        self.d_acc=self.Velo.a_dem*(self.Velo.t_dem**2)/2+self.Velo.a_suite*((self.t_acc-self.Velo.t_dem)**2)/2

def altitude(pos,tronçon):
    return ((tronçon[2]-tronçon[1])/tronçon[0])*pos+tronçon[1]

def decoupage_stops(chemin):
    chemin_new=[]
    for tronçon in chemin:
        tronçon_new=[]
        if len(tronçon[4])>0:
            for i,pos_stop in enumerate(tronçon[4]):
                if i==0:
                    tronçon_new+=[tronçon[4][0],tronçon[1],altitude(tronçon[4][0],tronçon),tronçon[3],True] #plus de stop. Premier stop.
                else:
                    tronçon_new+=[tronçon[4][i]-tronçon[4][i-1],altitude(tronçon[4][i-1],tronçon),altitude(tronçon[4][i],tronçon),tronçon[3],True]
        else:
            tronçon_new=tronçon[:]
            tronçon_new.pop()
            tronçon_new+=[True]       #remplacer la liste des stops qui sert à rien par le booléen dem
        chemin_new+=[tronçon_new]
    return chemin_new


def calcul_decoupe(chemin,Velo):
    res=[]
    chemin_calcul=decoupage_stops(chemin)
    for bout in chemin_calcul:
        road_type=Lieu(bout[3],Velo)
        data=Segment(Velo,bout[1],bout[2],bout[0],road_type,bout[4])
        res+=[(data.ene_wh_rap,data.pui_rap_max,data.time)] #energie,puissance max et temps du Segment
    return res


def calcul_tot(chemin,Velo,usager,puiss_max_cycliste):#cf PMA: 250W chez les cyclos peu entrainés, 500 chez les meilleurs (et les livreurs savent pédaler)
    res=calcul_decoupe(chemin,Velo)
    energy_tot=0
    time_overpowered=0
    powerlim=Velo.puiss_max+usager
    real_powerlim=Velo.puiss_max+puiss_max_cycliste
    for seg in res:
        energy_tot+=seg[0]
        if seg[1]>powerlim:
            if seg[1]>real_powerlim:
                return ("trajet impossible")
            elif seg[2]>5:
                return ("trajet trop fatiguant")
            else:
                time_overpowered+=seg[2]
    if time_overpowered>10:
        return ("trajet trop fatiguant")
    else:
        return (energy_tot,max([res[i][1] for i in range (len(res))]),chemin[0][3],res[0][2])#renvoie la somme des énergies de chaque Segment et la vitesse



def calcul_energy(chemin,Velo,usager,puiss_max_cycliste):
    res=calcul_tot(chemin,Velo,usager,puiss_max_cycliste)
    while isinstance(res,str)==True:
        if chemin[0][3]<2.8:
            return "vraiment impossible"
        else:
            chemin[0][3]=max(chemin[0][3]-1,2.8)
            if isinstance(calcul_tot(chemin,Velo,usager,puiss_max_cycliste),str)==True and chemin[0][3]==2.8:
                return "vraiment impossible"
            elif isinstance(calcul_tot(chemin,Velo,usager,puiss_max_cycliste),str)==False:
                return calcul_tot(chemin,Velo,usager,puiss_max_cycliste)
    return res









            #self.pui_suite_rap=max((1/rap)*(0.5*self.Velo.m*(self.Lieu.v**2-(self.Velo.a_dem*self.Velo.t_dem)**2)+9.81*self.Velo.m*sin(self.pente)*(self.Velo.a_dem*self.Velo.t_dem*(self.Lieu.t_acc-self.Velo.t_dem)+0.5*self.Velo.a_suite*((self.Lieu.t_acc-self.Velo.t_dem)**2)))-usager,0) #puissance demarrage phase 2, juste au cas où si je me suis trompé


