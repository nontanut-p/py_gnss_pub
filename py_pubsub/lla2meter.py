from math import *
import random

lat_0 = 14.0790659
lon_0 = 100.6014028
earth_radius = 6356752.3142    # meter


def meter2lla( x, y ):
  global lat_0, lon_0, earth_radius

#  y = (lat - lat_0) * pi/180.0 * earth_radius
  lat = y*180.0/(earth_radius*pi) + lat_0
  
  b = tan( x/(earth_radius*2) )**2
#  b - ab = a
  a = b/(b+1)
  
  c = asin( sqrt( a / cos(lat_0* pi/180.0)**2 ) ) * 180.0 / (0.5* pi)
  if x>0:
    c = abs(c)
  else:
    c = -abs(c)
  lon = c + lon_0
  return lat, lon


def lla2meter( lat, lon ):
  global lat_0, lon_0, earth_radius

#  y = distance( lat_0, lon_0, lat, lon_0 )
  y = (lat - lat_0) * pi/180.0 * earth_radius

#  x = distance( lat_0, lon_0, lat_0, lon )
  if lon > lon_0:
    sign = 1.0
  else:
    sign = -1.0
  a = cos(lat_0* pi/180.0)**2 * sin((lon-lon_0)*0.5* pi/180.0)**2
  x = 2 * atan2(sqrt(a), sqrt(1-a)) * earth_radius
  
  x = sign*abs(x)
  return x,y

 
# https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
# https://en.wikipedia.org/wiki/Haversine_formula
def distance(lat1, lon1, lat2, lon2):
  global earth_radius
  
  deg2rad = pi / 180.0
  lat1*= deg2rad
  lat2*= deg2rad
  lon1*= deg2rad
  lon2*= deg2rad

  a = sin((lat2-lat1)*0.5)**2 + \
    cos(lat1) * cos(lat2) * \
    sin((lon2-lon1)*0.5)**2
  c = 2 * atan2(sqrt(a), sqrt(1-a))
  return earth_radius * c


if __name__ == "__main__":
#  random.seed(2)

  
  lat = 14.0780659
  lon = 100.6034028
  x,y = lla2meter( lat, lon )
  lat2, lon2 = meter2lla( x, y )
  s = sqrt(x**2 + y**2)
  print( 'll: %.5f  %.5f ,  %.5f  %.5f' % (lat, lat2, lon, lon2 ) )
  print('  xy: %.3f  %.3f' % (x,y))
  print('  s : %.3f ' %s)
  print('  e : %.5f  %.5f' % (abs(lat - lat2), abs(lon - lon2 )) )
  if abs(lat-lat2) > 0.001 or abs(lon-lon2) > 0.001:
    print('fail')
    exit()
  '''
  lat1 = lat_0
  lon1 = lon_0
  lat2 = lat_0 + 1.0
  lon2 = lon_0 + 1.0
  
  x1,y1 = lla2meter(lat1, lon1)
  x2,y2 = lla2meter(lat2, lon2)
  
  print( sqrt( (x1-x2)**2 + (y1-y2)**2 ) )
  print( distance(lat1, lon1, lat2, lon2) )
  '''
  
  
  
  

