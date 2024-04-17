import requests
import datetime
from django.shortcuts import render

API_KEY = "38b99bbe57c19d30081034907de0bc40"
def application(request):
    api_key = "38b99bbe57c19d30081034907de0bc40"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    airpopulation_url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={}&lon={}&appid={}"
    try: 
        if request.method == "POST":
            city1 = request.POST['city1']
            city2 = request.POST.get('city2', None)

            if not city1:
                return render(request, "home.html", {'error': 'Please enter City 1'})
       
            weather_data1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)
            airpop_data1 = fetch_airpopulation(city1,API_KEY,current_weather_url,airpopulation_url)
            daily_forecast1 = get_5_day_forecast(city1,api_key)
            if city2:
                weather_data2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
                daily_forecast2 = get_5_day_forecast(city2,api_key)
                airpop_data2 = fetch_airpopulation(city2,API_KEY, current_weather_url,airpopulation_url)
            else:
                weather_data2 = None
                daily_forecast2 = None
                airpop_data2 = None

            context = {
                "weather_data1": weather_data1,
                "daily_forecasts1": daily_forecast1,
                "weather_data2": weather_data2,
                "daily_forecasts2": daily_forecast2,
                "airpop_data1": airpop_data1,
                "airpop_data2":airpop_data2,
                }

            return render(request, "home.html", context)
        else:
            return render(request, "home.html")
    except Exception as e:
         return render(request, 'home.html', {'err': "something went wrong"})

def fetch_airpopulation(city, api_key,weather ,airpopulationurl):
   
        city_data = requests.get(weather.format(city, api_key)).json()
        lat,lon = city_data['coord']['lat'], city_data['coord']['lon']
        data = requests.get(airpopulationurl.format(lat, lon, api_key)).json()
        components = data['list'][0]['components']
        airdata = {
            'co':components['co'],
            'no': components['no'],
            'no2': components['no2'],
            'o3': components['o3'],
            'so2':components['so2'],
            'pm2_5':components['pm2_5'],
            'pm10':components['pm10'],
            'nh3':components['nh3'],
            }
        return airdata
  
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetch current weather data
   
        current_response = requests.get(current_weather_url.format(city, api_key)).json()
        lat, lon = current_response['coord']['lat'], current_response['coord']['lon']

        # Fetch 5-day forecast data
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

        # Extract rain data if available
        rain_data = current_response.get('rain', {}).get('1h', 0)
        try:
             visi = current_response['visibility']
        except Exception as er:
             visi = None
        weather_data = {
            'city': city,
            'date': datetime.datetime.fromtimestamp(current_response['dt']).strftime("%d-%m-%Y"),
            'time': datetime.datetime.fromtimestamp(current_response['dt']).time(),
            'temperature': round(current_response['main']['temp'] - 273.15, 2),
            'description': current_response['weather'][0]['description'],
            'pressure': current_response['main']['pressure'],
            'humidity': current_response['main']['humidity'],
            'feelslike': round(current_response['main']['feels_like'] - 273.15, 2),
            'windspeed': current_response['wind']['speed'],
            'visibility': visi,
            'icon': current_response['weather'][0]['icon'],
            'lat': current_response['coord']['lat'],
            'lon': current_response['coord']['lon'],
            'rain': rain_data,  # Add rain data to the weather data
            }

        return weather_data
    


def get_5_day_forecast(city, API_KEY):
    
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
    
        daily_forecast = []
        forecast_dates = set()  # To keep track of dates already added to the forecast
    
        # Get tomorrow's date
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
        for forecast in data['list']:
            # Extract date from the forecast
            forecast_date = datetime.datetime.fromtimestamp(forecast['dt']).date()
        
         # Check if the forecast date is tomorrow or later
            if forecast_date >= tomorrow:
                # Check if the forecast date is already added
                if forecast_date not in forecast_dates:
                    daily_forecast.append({
                        'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
                        'min_temp' : round(forecast['main']['temp_min'] - 273.15, 2),
                        'max_temp': round(forecast['main']['temp_max'] - 273.15, 2),
                        'description': forecast['weather'][0]['description'],
                        'icon': forecast['weather'][0]['icon']
                        }) 
                # Add the forecast date to the set
                    forecast_dates.add(forecast_date)
    
        return daily_forecast
   



def map_view(request):
    return render(request, 'map.html')
# Extracting and printing min and max temperatures for each day

