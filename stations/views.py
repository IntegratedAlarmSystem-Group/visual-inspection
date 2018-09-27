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
    username_placeholder = ''
    form_login_message = ''
    vir_recorded = False
    recorded_stations = []
    non_recorded_stations = []
    selected_stations = False
    sent_inspection = False
    missing_username = False

    if request.method == 'POST':

            sent_inspection = True
            sent_valid_inspection = False

            username = request.POST['login']
            vir_stations_list = request.POST.getlist('vir')
            vir_stations_count = len(vir_stations_list)

            # check username and vir stations list
            if (username == '') or (username.isspace()):
                missing_username = True

            if missing_username:
                form_login_message = '* Required'

            selected_stations = (vir_stations_count > 0)

            if selected_stations:
                if not missing_username:
                    sent_valid_inspection = True

            # process inspection
            if sent_valid_inspection:
                # valid username and inspection available
                for station_name in vir_stations_list:
                    station = Station.objects.get_by_name(station_name)
                    if station is not None:
                        inspection = Inspection(station, username).save()
                        if inspection is not None:
                            recorded_stations.append(station_name)
                        else:
                            non_recorded_stations.append(station_name)
                    else:
                        non_recorded_stations.append(station_name)
            else:
                non_recorded_stations = vir_stations_list

            non_recorded_count = len(non_recorded_stations)
            recorded_count = len(recorded_stations)

            vir_recorded = (recorded_count)
            vir_recorded = vir_recorded and (recorded_count == vir_stations_count)
            vir_recorded = vir_recorded and (non_recorded_count == 0)

            if vir_recorded:
                # vir recorded
                message = 'Succesfull records for the VIR'
                username_placeholder = ''
            else:
                # no vir recorded
                message = 'Problem detected for the VIR'
                username_placeholder = username


    context['username'] = username_placeholder
    context['sent_inspection'] = sent_inspection
    context['result'] = message
    context['form_login_message'] = form_login_message
    context['recorded'] = vir_recorded
    context['recorded_stations'] = recorded_stations
    context['non_recorded_stations'] = non_recorded_stations
    context['selected_stations'] = selected_stations
    context['stations'] = sorted(stations, key=lambda k: k.name)

    request_context = RequestContext(request, context)

    return HttpResponse(t.template.render(request_context))
