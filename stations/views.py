from django.http import HttpResponse
from django.template import loader

STATIONS = [
    'MeteoTB1',
    'MeteoTB2',
    'MeteoItinerant',
    'Meteo201',
    'MeteoCentral',
    'Meteo309',
    'Meteo410',
    'Meteo131',
    'Meteo129',
    'Meteo130'
]

def index(request):

    stations_list = STATIONS
    template = loader.get_template('./index.html')
    context = {
        'stations': stations_list
    }

    return HttpResponse(template.render(context, request))
