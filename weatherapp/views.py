# Chatgt adjusted code
import urllib.request
import json
from django.shortcuts import render

from django.conf import settings

# Define your API key directly in the code
API_KEY = settings.API_KEY

def index(request):
    data = {}
    error = None
    unit = request.GET.get("unit", "metric")  # Default to Celsius
    unit_symbol = "°C" if unit == "metric" else "°F"

    if request.method == "POST":
        city = request.POST.get("city")

        if not city:
            error = "Please enter a city name."
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"

            try:
                with urllib.request.urlopen(url) as response:
                    source = response.read()
                    list_of_data = json.loads(source)

                    data = {
                        "city": city,
                        "country_code": list_of_data['sys']['country'],
                        "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                        "temp": f"{list_of_data['main']['temp']} {unit_symbol}",
                        "pressure": f"{list_of_data['main']['pressure']} hPa",
                        "humidity": f"{list_of_data['main']['humidity']}%",
                        "main": list_of_data['weather'][0]['main'],
                        "description": list_of_data['weather'][0]['description'].capitalize(),
                        "icon": f"http://openweathermap.org/img/wn/{list_of_data['weather'][0]['icon']}@2x.png",
                    }
            except Exception as e:
                error = "City not found. Please enter a valid city name."

    return render(request, "main/index.html", {"data": data, "error": error, "unit": unit, "unit_symbol": unit_symbol})


# import urllib.request
# import json
# from django.shortcuts import render
# # Create your views here.


# def index(request):
#     if request.method == 'POST':
#         city = request.POST['city']

#         source = urllib.request.urlopen('http://api-openweathermap.org/data/2.5/weather?q=' + city + '&appid=cba7c2bd0644a406da360516dfcf066a').read()
#         list_of_data = json.loads(source)

#         data = {
#             "country_code": str(list_of_data['sys']['country']),
#             "coordinate": str(list_of_data['coord']['lon']) + ', '
#             + str(list_of_data['coord']['lat']),

#             "temp": str(list_of_data['main']['temp']) + ' °C',
#             "pressure": str(list_of_data['main']['pressure']),
#             "humidity": str(list_of_data['main']['humidity']),
#             'main': str(list_of_data['weather'][0]['main']),
#             'description': str(list_of_data['weather'][0]['description']),
#             'icon': list_of_data['weather'][0]['icon'],
#         }
#         print(data)
#     else:
#         data = {}

#     return render(request, "main/index.html", data)