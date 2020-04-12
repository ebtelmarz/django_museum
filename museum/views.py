import csv
from typing import re

from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
from .models import Group
from .models import Visitor
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django import forms
import os
from datetime import datetime
from django.http import HttpResponseNotAllowed
from django.forms import FileInput as fi
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.template import loader, Context

# Create your views here.
# le views devono sempre ritornare una HttpResponde oppure exception!!

# return render(request, 'museum/home.html', context)
# il primo argomento di render è la request, il sedondo il path sotto la cartella templates
# dove deve prendere l'html, il terzo argomento sono i dati dinamici da caricare
# render ritorna una httpresponse in background

## VISITOR DI TEST 209_153

visitor = {
    'number': 209,
    'group_id': 153,
    'startTime': '11:55',
    'endTime': '12:34',
    'date': '21/8/2011',
    'blind': '20E',
    'headPhones': 1,
    'notes': '',
    'defect': ''
}

group = {
    'number': 153,
    'size': 3,
    'date': '21/8/2011'
}


def fileProcess(fileName):
    intero = open(fileName)

    context = {
        'summary': [],
        'locations': [],
        'mappa': []
    }

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

    ####################### SUMMARY DATA ##############################
    num_events = 0  # ma sti eventi che so?? le azioni registrate dal dispositivo?
    for line in events:
        if line.split(',')[1] == 'chosenExhibit':
            num_events += 1

    clean = []
    for pp in presentations:
        clean.append(pp.split(',')[2])

    n_presentations = len(set(clean))

    visitor = fileName.split('.')[0].split('_')[1]
    group = fileName.split('.')[0].split('_')[2]
    # aggiungere data della visita e dimensione del gruppo ?

    total = None
    global_start = positions[0].split(',')[0]
    global_end = positions[len(positions) - 1].split(',')[1]

    durata_delta = str(datetime.strptime(global_end, '%H:%M:%S') - datetime.strptime(global_start, '%H:%M:%S'))
    durata = None
    ore = str(durata_delta).split(':')[0]
    min = str(durata_delta).split(':')[1]
    sec = str(durata_delta).split(':')[2]
    pre = ''
    ## supponiamo che una visita non duri piu di 9 ore xd
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

    context.get('summary').append(
        {'start': global_start, 'end': global_end, 'num_pres': n_presentations,
         'duration': total, 'visitor': visitor, 'group': group, 'num_events': num_events})

    ####################### TIMELINE DATA #############################
    duration = None

    for record in positions:
        split = record.split(',')
        location = split[2]
        start = datetime.strptime(split[0], '%H:%M:%S')
        end = datetime.strptime(split[1], '%H:%M:%S')
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

        context.get('locations').append(
            {'start': str(start).split()[1], 'end': str(end).split()[1], 'position': location,
             'duration': duration, 'visitor': visitor, 'group': group})

    ############################ MAP DATA ##############################
    locations = Location.objects.all()
    for val2 in positions:
        for elem2 in locations:
            # print((elem2.x, val2[2]))

            if val2.split(',')[2] == elem2.name:
                x = elem2.x
                y = elem2.y

                context.get('mappa').append({'name': elem2.name, 'x': x, 'y': y})
    return context


def about(request):
    return render(request, 'museum/about.html')


def statistics(request):
    return render(request, 'museum/statistics.html')


def map(request):
    context = {
        'pos': Location.objects.all()
    }
    return render(request, 'museum/map.html', context)

def home(request):
    context = {
        'data': [],
        'locations': [],
        'mappa': [],
        'gruppo': Group.objects.all(),
        'visitor': Visitor.objects.all(),
        'summary': []
    }

    if request.method == 'POST':
        key = 'document'
        if key not in request.FILES:
            messages.warning(request, f'Please upload a log file')
        else:
            file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(file.name, file)

            context['url'] = fs.url(name)
            context['locations'] = fileProcess(os.path.join('media/', file.name))['locations']
            context['mappa'] = fileProcess(os.path.join('media/', file.name))['mappa']
            context['summary'] = fileProcess(os.path.join('media/', file.name))['summary']

            if 'map' in request.POST:
                return render(request, 'museum/map.html', context)
            elif 'stat' in request.POST:
                return render(request, 'museum/statistics.html', context)

    return render(request, 'museum/home.html', context)


# return redirect('museum-home')

"""

dati da ritornare:
    start e
    end per ogni posizione
    position
    duration per posizione
    
    dati summary:
    visitor
    group
    num presentazioni viste 
    start globale
    end globale --> durata totale 
    data della visita
    group size
"""

