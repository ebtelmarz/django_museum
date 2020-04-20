from os import listdir
from django.shortcuts import render
from django.http import HttpResponse
from .models import PointOfInterest
from .models import Visitor
from .models import Event
from .models import Position
from .models import Presentation
from django.core.files.storage import FileSystemStorage
import os
import csv
import json
import subprocess
from datetime import datetime, timedelta
from django.contrib import messages


# Create your views here.
# le views devono sempre ritornare una HttpResponde oppure exception!!

# return render(request, 'museum/home.html', context)
# il primo argomento di render è la request, il sedondo il path sotto la cartella templates
# dove deve prendere l'html, il terzo argomento sono i dati dinamici da caricare
# render ritorna una httpresponse in background

## VISITOR DI TEST 209_153

def prepareVisitor(path_visitors, presentations, interruptions, positions, group, visitor_id):
    visitor_data = []
    with open(path_visitors) as vis:
        reader = csv.reader(vis, delimiter=',')
        prima = next(reader)
        for line in reader:
            if line[0] == visitor_id:
                data = line[3]
                global_start = line[4] + ':00'
                global_end = line[5] + ':00'
            else:
                data = ''
                global_start = positions[0].split(',')[0]
                global_end = positions[len(positions) - 1].split(',')[1]

            visitor_data.append(
                (visitor_id, group, data, global_start, global_end, len(presentations), interruptions))

    return set(visitor_data)


def updatePOIS():
    map_json = json.load(open('media/map.json', 'r'))

    for line in map_json:
        route = line["Route"]
        for elem in route:
            pins = elem["PointsInRoute"]
            for val in pins:
                pin = val["PointInRoute"]
                for a in pin:
                    name = a["Point"]["_name"]
                    x = a["Point"]["_x"]
                    y = a["Point"]["_y"]
                    room = a["Point"]["_room"]
                    backName = a["Point"]["_backName"]

                    xx = int(int(x) * 1.15)
                    yy = int(int(y) * 1.1)

                    poi_obj = PointOfInterest(name=name, x=xx, y=yy, room=room, backName=backName)
                    poi_obj.save()


def saveData(visitor_data, presentations, events, positions):

    vis_obj = None
    interrupt = 0

    for vis in visitor_data:
        interrupt = vis[6]
        vis_obj = Visitor(number=vis[0], group=vis[1], date=vis[2], startTime=vis[3], endTime=vis[4], presentations=vis[5], interruptions=vis[6])
        vis_obj.save()

    for event in events:
        eve_obj = Event(when=event.split(',')[0], name=event.split(',')[1], visitor_id=vis_obj)
        eve_obj.save()

    for pres in presentations:
        pres_obj = Presentation(startTime=pres.split(',')[0], endTime=pres.split(',')[1], name=pres.split(',')[2], visitor_id=vis_obj)
        pres_obj.save()

    if len(PointOfInterest.objects.all()) == 0:
        updatePOIS()

    for pos in positions:
        pos_obj = Position(start=pos.split(',')[0], end=pos.split(',')[1], visitor_id=vis_obj, poi_id=PointOfInterest.objects.get(name=pos.split(',')[2]))
        pos_obj.save()


def prepareData():
    path_logs = 'media/logs'
    path_visitors = 'media/visitors.csv'
    files = os.listdir(path_logs)

    #try:
    #    files = list(filter(lambda a: a != 'out.log', files))
    #except:
    #    print('out.log not found')

    for fileName in files:
        visitor_id = fileName.split('.')[0].split('_')[1]

        if not Visitor.objects.filter(number=visitor_id).exists():
            try:
                group = fileName.split('.')[0].split('_')[2]
                intero = open(os.path.join(path_logs, fileName))

                positions = []
                presentations = []
                events = []

                stringone = ''
                for riga in intero:
                    stringone = stringone + str(riga)
                #################### EVENTS ######################################
                eventi = stringone.split('events ')[1]
                elem = eventi.split('\n')

                for val in elem:
                    events.append(val)
                try:
                    events = list(filter(lambda a: a != '', events))
                except:
                    print('not found')
                #################### PRESENTATIONS ################################
                presentazioni = stringone.split('presentations ')[1].split('events ')[0]
                pres = presentazioni.split('\n')

                for val in pres:
                    presentations.append(val)
                try:
                    presentations = list(filter(lambda a: a != '', presentations))
                except:
                    print('not found')
                interr = 0
                interruptions = 0
                interrupt = 0
                for b in presentations:
                    if b.split(',')[4] == 'User':
                        interr += 1
                if len(presentations) != 0:
                    interrupt = interr / int(len(presentations))
                    if interrupt > 0.5:
                        interruptions = 1
                else:
                    interruptions = 0
                #################### POSITIONS ####################################
                posizioni = stringone.split('presentations ')[0]
                pos = posizioni.split('\n')

                for val in pos:
                    positions.append(val)

                try:
                    positions = list(filter(lambda a: a != '', positions))
                    positions = list(filter(lambda a: a != 'Positions ', positions))
                except:
                    print('not found')

                visitor_data = prepareVisitor(path_visitors, presentations, interruptions, positions, group, visitor_id)
                saveData(visitor_data, presentations, events, positions)
            except:
                continue


def locationsData(number):
    timeline_data = []
    positions = Position.objects.filter(visitor_id_id=number)

    for pos in positions:
        location = pos.poi_id.name
        start = datetime.strptime(str(pos.start), '%H:%M:%S')
        end = datetime.strptime(str(pos.end), '%H:%M:%S')
        duration_delta = end - start
        min1 = str(duration_delta).split(':')[1]
        sec1 = str(duration_delta).split(':')[2]

        if min1[0] == '0':
            min1 = min1[1]
        if sec1[0] == '0':
            sec1 = sec1[1]

        if min1 == '0':
            duration = sec1 + ' seconds'
        else:
            if min1 == '1':
                duration = min1 + ' minute and ' + sec1 + ' seconds'
            else:
                duration = min1 + ' minutes and ' + sec1 + ' seconds'

        timeline_data.append(
            {'start': str(start).split()[1], 'end': str(end).split()[1], 'position': location,
             'duration': duration})

    return timeline_data


def summaryData(number):
    summary_data = []

    positions = Position.objects.filter(visitor_id_id=number)
    events = Event.objects.filter(visitor_id_id=number)
    group = Visitor.objects.get(number=number).group
    pres_count = len(Presentation.objects.filter(visitor_id=number))
    presses = Presentation.objects.filter(visitor_id=number)

    lista_pres = []
    for elem in presses:
        lista_pres.append(elem.name)

    lista_pres = set(lista_pres)
    num_locs = len(lista_pres)
    total = None
    global_start = str(positions[0].start)
    global_end = str(positions[len(positions) - 1].end)

    durata_delta = str(datetime.strptime(global_end, '%H:%M:%S') - datetime.strptime(global_start, '%H:%M:%S'))
    durata = None
    ore = str(durata_delta).split(':')[0]
    min = str(durata_delta).split(':')[1]
    sec = str(durata_delta).split(':')[2]
    #pre = ''

    if min[0] == '0':
        min = min[1]
    if sec[0] == '0':
        sec = sec[1]

    if int(ore) > 1:
        pre = ore + ' hours, '
    else:
        if int(ore) == 0:
            pre = ''
        else:
            pre = ore + ' hour, '

    if min == '0':
        durata = sec + ' seconds'
    else:
        if min == '1':
            durata = min + ' minute and ' + sec + ' seconds'
        else:
            durata = min + ' minutes and ' + sec + ' seconds'

    if pre != '':
        total = pre + durata
    else:
        total = durata

    somma = int(ore)*60 + int(min) + int(sec)/60

    tot = datetime.strptime('00:00:00', '%H:%M:%S')
    for id in Visitor.objects.all():
        visitor_stay = Position.objects.filter(visitor_id=id)
        diff = datetime.strptime(str(visitor_stay[len(visitor_stay) - 1].end), '%H:%M:%S') - datetime.strptime(str(visitor_stay[0].start), '%H:%M:%S')
        tot = tot + diff

    tot = datetime.strptime(str(tot.time()), '%H:%M:%S')
    tott = tot.hour*60 + tot.minute + tot.second/60
    avg_stay = tott/len(Visitor.objects.all())

    more_than_avg = 0
    str_avg = 'did not stay more than the average'
    if somma > avg_stay:
        more_than_avg = 1
        str_avg = 'stayed more than the average'

    interrupt = Visitor.objects.get(number=number).interruptions

    str_interr = 'did not interrupt a lot of presentations'
    if interrupt > 0:
        str_interr = 'interrupted more than half of the presentations'
    tot_count = 0

    for person in Visitor.objects.all():
        conta = len(Presentation.objects.filter(visitor_id=person.number))
        tot_count += conta
    avg_present = tot_count/len(Visitor.objects.all())

    more_than_avg_p = 0
    str_pres = 'didn\'t watch more presentations than the average'
    if pres_count > avg_present:
        more_than_avg_p = 1
        str_pres = 'watched more presentations than the average'

    liked = ' did not enjoy '
    if more_than_avg + more_than_avg_p - interrupt >= 1:
        liked = ' enjoyed '

    summary_data.append(
        {'start': global_start, 'end': global_end, 'num_pres': pres_count, 'num_locs': num_locs,
         'duration': total, 'visitor': number, 'group': group, 'presentations': lista_pres, 'liked': liked,
         'str_pres': str_pres, 'str_avg': str_avg, 'str_interr': str_interr})

    return summary_data


def mapData(number):
    map_data = []
    positions = Position.objects.filter(visitor_id=number)

    for pos in positions:
        name = pos.poi_id.name
        x = PointOfInterest.objects.get(name=name).x
        y = PointOfInterest.objects.get(name=name).y

        map_data.append({'name': name, 'x': x, 'y': y})

    return map_data


def about(request):
    return render(request, 'museum/about.html')


def statistics(request):
    return render(request, 'museum/statistics.html')


def map(request):
    context = {
        'pos': PointOfInterest.objects.all()
    }
    return render(request, 'museum/map.html', context)


def home(request):
    context = {
        'summary': []
    }

    if request.method == 'POST':
        if 'upload' in request.POST:
            if 'document' not in request.FILES:
                messages.warning(request, f'Please upload a log file')
            else:
                file = request.FILES['document']
                if str(file.name).split('.')[1] != 'csv':
                    messages.warning(request, f'Please upload a valid csv file')
                else:
                    if file.name not in os.listdir('media/logs'):
                        fs = FileSystemStorage()
                        name = fs.save(file.name, file)
                        context['url'] = fs.url(name)
                        messages.info(request, f'File uploaded correctly')
                    else:
                        messages.info(request, f'File already exists')

        if 'refresh' in request.POST:
            prepareData()
            messages.info(request, f'Done!')
            return render(request, 'museum/home.html', {'visitors': Visitor.objects.all()})

        if 'map' in request.POST:
            if request.POST['drop'] == 'Choose...':
                messages.warning(request, f'Please choose a visitor')
            else:
                data = {
                    'mappa': mapData(request.POST['drop']),
                    'timeline': locationsData(request.POST['drop']),
                    'summary': summaryData(request.POST['drop'])
                }
                map = locationsData(request.POST['drop'])
                return render(request, 'museum/map.html', data)

        elif 'stat' in request.POST:
            if request.POST['drop'] == 'Choose...':
                messages.warning(request, f'Please choose a visitor')
            else:
                return render(request, 'museum/statistics.html', context)

    return render(request, 'museum/home.html', {'visitors': Visitor.objects.all()})


# return redirect('museum-home')

