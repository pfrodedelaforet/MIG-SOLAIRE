def s(clients,graphe,i,j,elp): #C'est un Poids ,s permet l'optimisation des tournees c'est une matrice len(pts)² ,i et j sont des indices, clients une liste de DeliveryPoint
    return(graphe[clients[i]][elp] + graphe[elp][clients[j]] - graphe[clients[i]][clients[j]])
        
#optimisation en utilisant une methode de TSP        
def cost_change(dst,pts, n1, n2, n3, n4):
    return dst(pts[n1],pts[n3]) + dst(pts[n2],pts[n4]) - dst(pts[n1],pts[n2]) - dst(pts[n3],pts[n4])

def two_opt(dst,pts,route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                if cost_change(dst,pts, best[i - 1], best[i], best[j - 1], best[j]) < 0:
                    best[i:j] = best[j - 1:i - 1:-1]
                    improved = True
        route = best
    return best
#fin TSP

def separer(dst,elps,clients): #Sorte de Voronoi en n²
    seplist = [[elps[i]] for i in range(len(elps))]#le premier element de seplist[i] est le point correspondant à elp[i]
    for i in clients:
        d = [(dst(i,elps[j]),j) for j in range(len(elps))]
        elp = min(d,key = lambda x:x[0])[1]
        seplist[elp].append(i)
    return seplist

def flatten(l): #a Liste Liste  -> a Liste
    nl = []
    for i in l:
        nl = nl + i
    return(nl)

def delkey(d,k):
    if k in d:
        del d[k]
        
def merge(clients,i,j,sw,ew):#sw et ew sont des dictionnaires cles : indices ,value: tournee. On fusionne la route qui finit par i avec celle qui commence par j
    tourn1,tourn2 = ew[i],sw[j]
    si,ej = tourn1.indices[0],tourn2.indices[-1]
    delkey(ew,i)
    delkey(ew,ej)
    delkey(sw,si)
    delkey(sw,j)
    ntourn = tourn1 + tourn2
    ew[ej] = ntourn
    sw[si] = ntourn
    
def req(triporteur,tourn):
    return(tourn.masse <= triporteur.capacity and all(map(lambda x: tourn.clients[x].t1 <= tourn.temps[x] <= tourn.clients[x].t2,range(len(tourn.clients)))) and (tourn.poids.energie <= triporteur.charge))

def Clarke(triporteurs,graphe,clients,elp,t0 = 0,requierements = req,ponderation = lambda x: x.energie):
    n = len(clients)
    tri0 = triporteurs[0]
    gains = flatten([[((i,j),s(clients,graphe,i,j,elp)) for i in range(n) if i != j] for j in range(n)])
    gains.sort(key = ponderation,reverse = True)# Ce sont les gains potentiels, on adopte une strategie gloutonne en privilegiant les gains les plus gros.
    sw = {}
    ew = {}
    for i in range(n):
        sw[i] = Tournee(clients,graphe,elp,i)
        ew[i] = Tournee(clients,graphe,elp,i)
    while True:
        if len(gains) == 0:
            break
        if i in ew and j in sw and j != ew[i].indices[0]:#si les tournees existent et sont differentes
            tfus = ew[i] + sw[j]
            if requirements(tri0,tfus):
                merge(clients,i,j,sw,ew)
            else:
                del gains[0]
        else:
            del gains[0]
            
    l = []
    for i in sw.values():
        l.append(two_opt(ponderation,clients,i.indices),i.poids)
        
    l.sort(key = lambda x:ponderation(x[1]),reverse = True)
    
    for tripo in triporteurs:
        if len(l) == 0:
            break
        else:
            if tripo.tournee == []:
                tripo.tournee = map(lambda x:clients[x],l[0][0])
                del l[0]
