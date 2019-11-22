from pyproj import Transformer
import math
transformer_to_lamb= Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

x_0,y_0=transformer_to_lamb.transform(7.26528, 43.69422 )
x_fin,y_fin=transformer_to_lamb.transform(7.28018,43.70168)

def conversion(lat,longi):
    x_lamb,y_lamb=transformer_to_lamb.transform(lat,longi)
    return (x_lamb-x_0,y_lamb-y_0)

def conv2(lat_deg,lon_deg):
  lat_rad = math.radians(lat_deg)
  x = (lon_deg + 180.0) / 360.0
  y = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 
  return x,y

#lat = 43.69795
#longi = 7.26763
#print(conversion(lat,longi),conv2(lat,longi))


