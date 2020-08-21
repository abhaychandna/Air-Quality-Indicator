from django.shortcuts import render
from django.http import HttpResponse
import datetime
from urllib.request import urlopen
import requests
import json
import math

AIR_POLLUTION_APIKEY = "change_this"
#FESTIVE_APIKEY = ""


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # in km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d



# Create your views here.
def home(request):
    cont = "x"
    context = {}
    template_name = "base.html"
    
    #FREEGEOIP
    url = "https://freegeoip.app/json/"

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }

    response = requests.request("GET", url, headers=headers)
    
    #print(response.text)
    #print(type(response.text))
    k = response.json()
    k2 = k
    #print(k)
    #print(type(k))
    latitude_num = k['latitude']
    longitude_num = k['longitude']
    #print(latitude,longitude)
    
    ## set to 6 decimal places
    latitude = str(latitude_num)
    longitude = str(longitude_num)
    latitude = latitude + "00"
    longitude = longitude + "00"
    context['latitude'] = latitude
    context['longitude'] = longitude
    context['geo'] = k2
    
    #AIRPOLLUTIONAPI COMBINED WITH LATITUDES FROM FREE GEOIP
    url = "http://api.airpollutionapi.com/1.0/aqi?lat=%s&lon=%s&APPID=%s" % (latitude,longitude,AIR_POLLUTION_APIKEY)

    #print(url)
    
    response = requests.request("GET",url)
    print(response.json())
    print(type(response.json()))
    k = response.json()
    cont = k['data']['clouds'] 
    context['aqi'] = k
    print("air",k)


    '''
    #HOLDIAYAPI 
    year = datetime.date.today().year
    month = datetime.date.today().month
    year = str(year)
    moth = str(month)
    
    url = "https://getfestivo.com/v2/holidays?api_key=%s&country=IN&year=%s&month=%s" % (FESTIVE_APIKEY,year,month) #CHANGE COUNTRY FROM LOCATION
    
    print(url)
    
    #response = requests.request("GET",url)
    #k = response.json()
    #cont = k["holidays"][0]["name"] 
    #context['holidays'] = k['holidays']
   
    

    #ISS API
    url = "http://api.open-notify.org/iss-now.json"

    response = urlopen(url)
    k = json.loads(response.read())

    iss_latitude_num = float(k['iss_position']['latitude'])
    iss_longitude_num = float(k['iss_position']['longitude'])
    iss_latitude = str(iss_latitude_num) + "00"
    iss_longitude = str(iss_longitude_num) + "00"
    print(type(iss_latitude_num),type(latitude_num))
    iss_dist_num = distance((latitude_num,longitude_num),(iss_latitude_num,iss_longitude_num))
    context["iss_latitude"] = iss_latitude
    context['iss_longitude'] = iss_longitude
    context['dist'] = iss_dist_num
    #print(type(context['holidays']))
    #print(context)
    '''

    #setting colors of AIR_POLLUTION_API
    for i in context['aqi']['data']['aqiParams']:
        #print("aqiParam")
        #print(i['color'])
        if i['color'] == 'red':
            i['color'] = "#ff5533"
            print(i['color'])
    print(context['geo'])
    return render(request,template_name,context)# %s",response.text)
