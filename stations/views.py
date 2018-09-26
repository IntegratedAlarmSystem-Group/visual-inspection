from django.http import HttpResponse
from django.template import loader

from stations.models import Station

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

    stations = Station.objects.all()
    template = loader.get_template('./index.html')
    context = {
        'stations': stations
    }

    return HttpResponse(template.render(context, request))
