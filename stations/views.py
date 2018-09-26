from django.http import HttpResponse
from django.template import loader

from stations.models import Station

def index(request):

    stations = Station.objects.all()
    template = loader.get_template('./index.html')
    context = {
        'stations': sorted(stations, key=lambda k: k.name) 
    }

    return HttpResponse(template.render(context, request))
