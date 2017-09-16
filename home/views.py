from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Crowdedness
from .models import Wifi
from .models import Noise

from .db import _db
from .generateGeoJSON import _generateGeoJSON

import json
# from django.utils.dateformat import format
# print format(mymodel.mydatefield, 'U')

# Create your views here.
from datetime import datetime, timedelta

@csrf_exempt
def db(request):
	if request.method == "POST":
		return HttpResponse(_db().store(request.POST));

    # return render(request, 'index.html')


def index(request):

    # greeting = Greeting()
    # greeting.save()

    data = Crowdedness.objects.all()
    # geoJSON_tup = _generateGeoJSON([1.352083], [103.819836], [156]).get()
    name = list(map(lambda x: x.name, data))
    type = list(map(lambda x: x.type, data))
    lat = list(map(lambda x: float(x.lat), data))
    lng = list(map(lambda x: float(x.lng), data))
    crowdedness = list(map(lambda x: x.crowdedness, data))
    geoJSON_tup = _generateGeoJSON(name, type, lat, lng, crowdedness).get()
    geoJSON = geoJSON_tup[0]
    min_crowdedness = geoJSON_tup[1]
    max_crowdedness = geoJSON_tup[2]


    return render(request, 'index.html', {'data': data, 'geoJSON': geoJSON, 'min_crowdedness': min_crowdedness, 'max_crowdedness': max_crowdedness})
    #return HttpResponse(geoJSON)

@csrf_exempt
def query(request):

    data = Crowdedness.objects.all()
    # geoJSON_tup = _generateGeoJSON([1.352083], [103.819836], [156]).get()
    name = list(map(lambda x: x.name, data))
    type = list(map(lambda x: x.type, data))
    lat = list(map(lambda x: float(x.lat), data))
    lng = list(map(lambda x: float(x.lng), data))
    crowdedness = list(map(lambda x: x.crowdedness, data))
    geoJSON_tup = _generateGeoJSON(name, type, lat, lng, crowdedness).get()
    geoJSON = geoJSON_tup[0]
    min_crowdedness = geoJSON_tup[1]
    max_crowdedness = geoJSON_tup[2]


    # return HttpResponse('Hello from Python!')
    # f=open("bot_debug.txt", "a+")
    # f.write(json.dumps(request.POST))
    # f.close()
    debug = {"content": request.POST}
    print(json.dumps(debug))
    req = request.POST['location']
    try:
        ret = Crowdedness.objects.get(nameStr=req)
        # scale
        _bin = (max_crowdedness - min_crowdedness) / 5
        _crowdedness = 0;
        if ret.crowdedness < min_crowdedness + _bin:
            _crowdedness = 1
        elif ret.crowdedness < min_crowdedness + _bin * 2:
            _crowdedness = 2
        elif ret.crowdedness < min_crowdedness + _bin * 3:
            _crowdedness = 3
        elif ret.crowdedness < min_crowdedness + _bin * 4:
            _crowdedness = 4
        else:
            _crowdedness = 5
        ret2 = {"nameStr": ret.nameStr, "crowdedness": _crowdedness}
        return HttpResponse(json.dumps(ret2))
    except Exception:
        return HttpResponse(status=404)

@csrf_exempt
def updateWifi(request):
    if 'mag' in request.POST:
        mag = request.POST['mag']
        Wifi(mag = mag).save()
        noises = Noise.objects.all().order_by('-when')[0:1]
        if len(noises) == 0:
            res = mag
        else:
            res = (float(mag) + float(noises[0].mag)) / 2

        blk71 = Crowdedness.objects.get(nameStr='star vista gallery hall')
        blk71.crowdedness = round(res)
        blk71.save()

        return HttpResponse('Wifi Updated')
    else:
        return HttpResponse(status=406)

@csrf_exempt
def updateNoise(request):
    if 'mag' in request.POST:
        mag = request.POST['mag']
        Noise(mag = mag).save()
        wifis = Wifi.objects.all().order_by('-when')[0:1]
        if len(wifis) == 0:
            res = mag
        else:
            res = (float(mag) + float(wifis[0].mag)) / 2

        blk71 = Crowdedness.objects.get(nameStr='star vista gallery hall')
        blk71.crowdedness = round(res)
        blk71.save()

        return HttpResponse('Noise Updated')
    else:
        return HttpResponse(status=406)

def dashboard(request):
    timestamp_to = datetime.now().date()
    timestamp_from_hour = datetime.now().date() - timedelta(hours=1)
    # timestamp_from_day = datetime.now().date() - timedelta(days=1)
    # timestamp_from_week = datetime.now().date() - timedelta(days=7)

    # acoustic_last_10 = Noise.objects.all().order_by('-when')[:10];
    acoustic_last = Noise.objects.all().order_by('-when')[0:1]
    acoustic_from_hour = Noise.objects.all().filter(when__gte = timestamp_from_hour)
    # acoustic_from_day = Noise.objects.all().filter(when__gte = timestamp_from_day)
    # acoustic_from_week = Noise.objects.all().filter(when__gte = timestamp_from_week)

    def helper(x):
        if x.mag <= 0:
            return 1
        elif x.mag >= 6:
            return 5
        else:
            return x.mag

    if len(acoustic_last) == 0:
        ac_avg = 0
    else:
        # ac_avg = sum(map(helper, acoustic_last_10)) / len(acoustic_last_10);
        # ac_avg = max(map(helper, acoustic_last))
        ac_avg = acoustic_last[0].mag

    # wifi_last_10 = Wifi.objects.all().order_by('-when')[:10]
    wifi_last = Wifi.objects.all().order_by('-when')[0:1]
    wifi_from_hour = Wifi.objects.all().filter(when__gte = timestamp_from_hour)
    # wifi_from_day = Wifi.objects.all().filter(when__gte = timestamp_from_day)
    # wifi_from_week = Wifi.objects.all().filter(when__gte = timestamp_from_week)

    if len(wifi_last) == 0:
        wf_avg = ac_avg
    else:
        # wf_avg = sum(map(helper, wifi_last_10)) / len(wifi_last_10);
        # wf_avg = max(map(helper, wifi_last))
        wf_avg = wifi_last[0].mag

    avg = (ac_avg + wf_avg) / 2

    return render(request, 'dashboard.html', {'avg': avg, 'acoustic_from_hour': acoustic_from_hour, 'wifi_from_hour': wifi_from_hour})

@csrf_exempt
def deletealldata(request):

    if request.method == "POST" and 'action' in request.POST and request.POST['action'] == 'delete':
        Crowdedness.objects.all().delete()
        Wifi.objects.all().delete()
        Noise.objects.all().delete()    
        return HttpResponse('All data deleted')
    else:
        return HttpResponse(status = 500)

@csrf_exempt
def deletecrowdedness(request):

    if request.method == "POST" and 'action' in request.POST and request.POST['action'] == 'delete':
        Crowdedness.objects.all().delete()
        return HttpResponse('All crowdedness data deleted')
    else:
        return HttpResponse(status = 500)

def getcrowdedness(request):
    cr = Crowdedness.objects.get(nameStr='star vista gallery hall').crowdedness
    return HttpResponse(cr)



