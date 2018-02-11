# -*- coding: utf-8 -*-
import json
import urllib.request as urllib2

from django.templatetags.static import static

from weather.models import Country


def weather_by_city_id(city_id):

    url_template = 'http://api.openweathermap.org/data/2.5/weather?id={}&appid={}'
    WEATHER_API_KEY = 'fca1cea44f1d503c0fc7ed168837c7b1'
    url = url_template.format(city_id, WEATHER_API_KEY)
    try:
        response = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return dict(error=True)

    data = json.loads(response)

    city_weather = dict(error=False)
    city_weather['city_name'] = data['name']
    city_weather['country_name'] = Country.objects.get(code=data['sys']['country']).name
    city_weather['weather'] = data['weather'][0]['main']
    city_weather['weather_description'] = data['weather'][0]['description']
    city_weather['temperature'] = int(round(data['main']['temp'] - 273.15))
    city_weather['humidity'] = int(round(data['main']['humidity']))
    city_weather['pressure'] = int(round(data['main']['pressure']))
    city_weather['wind_speed'] = int(round(data['wind']['speed']))



    return city_weather
