from django.shortcuts import render # type: ignore
import requests
import json
from django.conf import settings
# Create your views here.

from django.shortcuts import render
import requests
import json


def home(request):

    API_KEY = settings.WEATHER_API_KEY
    url = "https://api.weatherapi.com/v1/forecast.json"
    city_get = request.GET.get('city', '').strip()

    current = None
    forecast_data = None
    error = None


    if city_get:
        params = {
            'key': API_KEY,
            'q': city_get,
            'days': 7,
            'aqi': 'no'
        }

        response = requests.get(url, params=params)
        data = response.json()


        # API Error handling
        if "error" in data:
            error = data["error"]["message"]

        else:
            current = {
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "region": data["location"]["region"],
                "local_time": data["location"]["localtime"][11:16],

                "longitude": data["location"]["lon"],
                "latitude": data["location"]["lat"],

                "temp_c": data["current"]["temp_c"],
                "feels_like_c": data["current"]["feelslike_c"],

                "condition": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"],

                "cloud": data["current"]["cloud"],
                "humidity": data["current"]["humidity"],
                "wind_kph": data["current"]["wind_kph"],
                "wind_dir": data["current"]["wind_dir"],
                "visibility": data["current"]["vis_km"],
                "pressure_mb": data["current"]["pressure_mb"],
            }


            forecast_data = []

            for day in data["forecast"]["forecastday"]:

                forecast_data.append({
                    "date": day["date"],
                    "max_temp": day["day"]["maxtemp_c"],
                    "min_temp": day["day"]["mintemp_c"],
                    "condition": day["day"]["condition"]["text"],
                    "icon": 'https:' + day["day"]["condition"]["icon"]
                })


    context = {
        "current": current,
        "forecast": forecast_data,
        "error": error
    }


    return render(request, 'home.html', context)