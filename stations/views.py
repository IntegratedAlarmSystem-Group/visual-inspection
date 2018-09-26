import datetime

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

from stations.models import Station, Inspection


@csrf_protect
def inspection(request):

    stations = Station.objects.all()

    t = loader.get_template('./inspection.html')

    context = {}

    message = ''
    form_login_message = ''
    vir_recorded = False
    recorded_stations = []
    non_recorded_stations = []
    sent_inspection = False
    missing_username = False

    if request.method == 'POST':

            username = request.POST['login']
            vir_stations_list = request.POST.getlist('vir')

            # check username and vir stations list

            if (username == '') or (username.isspace()):
                missing_username = True

            if len(vir_stations_list) > 0:
                sent_inspection = True

            # process inspection

            if not missing_username:

                if sent_inspection:
                    # valid username and inspection available
                    for station_name in vir_stations_list:
                        station = Station.objects.get_by_name(station_name)
                        if station is not None:
                            inspection = Inspection(station).save()
                            if inspection is not None:
                                recorded_stations.append(station_name)
                            else:
                                non_recorded_stations.append(station_name)
                        else:
                            non_recorded_stations.append(station_name)

                # else: valid username but no inspection to process

            # else: data should not be processed (username is required)

            vir_recorded = (len(non_recorded_stations) == 0)
            if vir_recorded:
                message = 'Succesfull records for the VIR'
            else:
                message = 'Problem detected for the VIR'

            if missing_username:
                form_login_message = '* Required'

    context['sent_inspection'] = sent_inspection
    context['result'] = message
    context['form_login_message'] = form_login_message
    context['recorded'] = vir_recorded
    context['recorded_stations'] = recorded_stations
    context['non_recorded_stations'] = non_recorded_stations
    context['stations'] = sorted(stations, key=lambda k: k.name)

    request_context = RequestContext(request, context)

    return HttpResponse(t.template.render(request_context))
