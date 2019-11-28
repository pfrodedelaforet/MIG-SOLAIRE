from pyproj import Transformer
transformer_to_lamb= Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
transformer_to_lat_long=Transformer.from_crs( "EPSG:2154","EPSG:4326", always_xy=True)

def meterstoroute(point1, point2):#on prend en argument les coord metriques 
    start = Point(transformer_to_lat_long.transform(point1[O],point1[1])[0], transformer_to_lat_long.transform(point1[O],point1[1])[1]).id # Find start and end nodes
    end = Point(transformer_to_lat_long.transform(point2[O],point2[1])[0], transformer_to_lat_long.transform(point2[O],point2[1])[1]).id
    status, route = router.doRoute(start, end)
    l = 0
    for i in range(len(route)-1):
        point1 = Point(router.rnodes[route[i]][0],router.rnodes[route[i]][1]) 
        point2 = Point(router.rnodes[route[i+1]][0],router.rnodes[route[i+1]][1])
        l += router.distance((point1.latitude, point1.longitude),(point2.latitude, point2.longitude))
    return l * 1000