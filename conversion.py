from pyproj import Transformer
import math
transformer_to_lamb_aff= Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
transformer_to_lamb= Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)


lat = 43.6942
longi = 7.2652

delta_lat = 0.00746
delta_lon = 0.0149
x_0,y_0=transformer_to_lamb.transform(longi,lat)
x_fin,y_fin=transformer_to_lamb.transform(longi + delta_lon,lat + delta_lat)

#x_0,y_0=transformer_to_lamb.transform(
#x_fin,y_fin=transformer_to_lamb.transform(7.28018,43.70168)

def conversion(lati,longi):
    x_lamb,y_lamb=transformer_to_lamb.transform(longi,lati)
    return (y_lamb,x_lamb)

def conversion_aff(lati,longi):
    x_lamb,y_lamb=transformer_to_lamb_aff.transform(longi,lati)
    return (y_lamb,x_lamb)

def conv2(lat_deg,lon_deg):
  n = 2**zoom
  lat_rad = math.radians(lat_deg)
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

  return x,y

#lat = 43.69795
#longi = 7.26763
#print(conversion(lat,longi),conv2(lat,longi))

#def y2lat(a):
#  return 180.0/math.pi*(2.0*math.atan(math.exp(a*math.pi/180.0))-math.pi/2.0)
def lat2y(a):
  r = math.tan(math.pi/4 + a*(math.pi/180)/2)
  return math.log(r)*6378137
def lon2x(a):
    return math.radians(a)*6378137.0
