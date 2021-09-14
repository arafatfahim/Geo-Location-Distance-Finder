import re
from django.contrib.gis.geoip2 import GeoIP2

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

def get_center_cor(latA, lonA, latB=None, lonB=None):
    cord= (latA, lonA)

    if latB:
        cord =[(latA+latB)/2, (lonA+lonB)/2]
    return cord

def get_zoom(distance):
    if distance <=100:
        return 9
    elif distance > 100 and distance <=5000:
        return 7
    else:
        return 2

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip =x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip