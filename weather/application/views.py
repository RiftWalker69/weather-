import requests
import datetime
from django.shortcuts import render

def application(request):
    API_KEY = "38b99bbe57c19d30081034907de0bc40"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)
        weather_data1, forecast_data1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, forecast_data2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, forecast_data2 = None, None

        context = {
            "weather_data1": weather_data1,
            "forecast_data1": forecast_data1,
            "weather_data2": weather_data2,
            "forecast_data2": forecast_data2
        }
        return render(request, "home.html", context)
    else:
        return render(request, "home.html")

def fetch_weather_and_forecast(city, api, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    
    forecast_res = requests.get(forecast_url.format(lat, lon, api)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }

    daily_forecast = []
    # Check if 'daily' key exists in the forecast response
    if 'daily' in forecast_res:
        for data in forecast_res['daily'][:5]:
            daily_forecast.append({
                "day": datetime.datetime.fromtimestamp(data['dt']).strftime("%A"),
                "min_temp": round(data['temp']['min'] - 273.15, 2),
                "max_temp": round(data['temp']['max'] - 273.15, 2),
                "description": data['weather'][0]['description']
            })
    else:
        # Handle case where 'daily' key is not found
        daily_forecast = None
    
    return weather_data, daily_forecast
