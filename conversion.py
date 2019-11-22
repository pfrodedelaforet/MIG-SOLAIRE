from pyproj import Transformer
transformer_to_lamb= Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

x_0,y_0=transformer_to_lamb.transform(7.26528, 43.69422 )
x_fin,y_fin=transformer_to_lamb.transform(7.28018,43.70168)

def conversion(lat,long):
    x_lamb,y_lamb=transformer_to_lamb.transform(lat,long)
    return (x_lamb-x_0,y_lamb-y_0)
