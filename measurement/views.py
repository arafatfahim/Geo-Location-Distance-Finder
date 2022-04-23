from django.shortcuts import render, get_object_or_404
from geopy import location
from geopy import distance
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from .utils import *


# Create your views here.

def calculate_des_view(request):
    # initvale
    distance = None
    destination = None
    # obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurement')
    ip = get_ip(request)
    # print(ip_)
    # ip = '103.25.120.190'
    country, city, lat, lon = get_geo(ip)
    # print('location country', country)
    # print('location city', city)
    # print('location lat', lat, lon)

    location = geolocator.geocode(city)
    # print('###', location)
    # loc cordinate
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)
    # folium
    m = folium.Map(width=1080, height=720, location=get_center_cor(l_lat, l_lon))
    # location marker
    folium.Marker([l_lat, l_lon],
                  tooltip='click here for more', popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)
    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        # print(destination)
        # des cordinate
        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat, d_lon)
        # calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium
        m = folium.Map(width=800, height=500, location=get_center_cor(l_lat, l_lon, d_lat, d_lon),
                       zoom_start=get_zoom(distance))
        # location marker
        folium.Marker([l_lat, l_lon],
                      tooltip='click here for more', popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)
        # dest marker
        folium.Marker([d_lat, d_lon],
                      tooltip='click here for more', popup=destination,
                      icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        # draw line
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='red')
        m.add_child(line)
        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': distance,
        'destination': destination,
        'form': form,
        'map': m,
        'ip': ip,
    }

    return render(request, 'measurements/main.html', context)
