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
"""
mappa = [
    {
        'name': 'MaterialCultures',
        'x': '1868',
        'y': '1210'
    },
    {
        'name': 'EntranceReubenHecht',
        'x': '2746',
        'y': '1687'
    },
    {
        'name': 'ShipFront',
        'x': '688',
        'y': '571'
    }
]
"""


def about(request):
    return render(request, 'museum/about.html')


def statistics(request):

    # qua è ancora tutto da TODO-are

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
        'summary': []
    }

# mancano ancora i dati per la mappa, fare il match sul nome della posizione e prendere le coordinate dal db
# spostare il processing del file in una funzione a parte ??
# TODO

    if request.method == 'POST':
        key = 'document'
        if key not in request.FILES:
            messages.warning(request, f'Please upload a log file')
        else:
            file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(file.name, file)
            context['url'] = fs.url(name)

            positions = []
            presentations = []
            events = []

            intero = open(os.path.join('media/', file.name))
            stringone = ''
            for riga in intero:
                stringone = stringone + str(riga)

            #################### EVENTS ######################################
            eventi = stringone.split('events ')[1]
            elem = eventi.split('\n')

            for val in elem:
                events.append(val)

            events = list(filter(lambda a : a != '', events))

            #################### PRESENTATIONS ################################
            presentazioni = stringone.split('presentations ')[1].split('events ')[0]
            pres = presentazioni.split('\n')

            for val in pres:
                presentations.append(val)
            presentations = list(filter(lambda a: a != '', presentations))

            # presentations e events non servono a nulla in questa vivita a parte contare il numero di
            # presentazioni a cui ha partecipato il visitor, sono da passare alla view per le statitistiche
            # salvare nel context e passare tutto il context con una get a statistics
            # TODO


            #################### POSITIONS ####################################
            posizioni = stringone.split('presentations ')[0]
            pos = posizioni.split('\n')

            for val in pos:
                positions.append(val)

            positions = list(filter(lambda a: a != '', positions))
            positions = list(filter(lambda a: a != 'Positions ', positions))

            ####################### SUMMARY DATA ##############################
            num_events = 0                          # ma sti eventi che so?? le azioni registrate dal dispositivo
            for line in events:
                if line.split(',')[1] == 'chosenExhibit':
                    num_events += 1

            clean = []
            for pp in presentations:
                clean.append(pp.split(',')[2])

            n_presentations = len(set(clean))

            visitor = file.name.split('.')[0].split('_')[1]
            group = file.name.split('.')[0].split('_')[2]
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
                    #print((elem2.x, val2[2]))

                    if val2.split(',')[2] == elem2.name:
                        x = elem2.x
                        y = elem2.y
                        context.get('mappa').append({'name': elem2.name, 'x': x, 'y': y})

            return render(request, 'museum/map.html', context)

            # come gestire la doppia post nella home con il button che dovrebbe reindirizzare alle statistiche
            # TODO

    return render(request, 'museum/home.html', context)


# return redirect('museum-home')

"""

dati da ritornare:
    start e
    end per ogni posizione
    position
    duration per posizione
    
    dati summary;
    visitor
    group
    num presentazioni viste 
    start globale
    end globale --> durata totale 






            avoid = ['e', 'p', 'P', 'E']
            avoid_events = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            
            with open(os.path.join('media/', file.name)) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                prima = next(reader)
                if next(reader)[0] in avoid:
                    next(reader)

                duration = None
                start = None
                end = None

                for line in reader:
                    try:
                        if line[0][0] == '':
                            break

                        position = line[2]

                        start = datetime.strptime(line[0], '%H:%M:%S')
                        end = datetime.strptime(line[1], '%H:%M:%S')
                        duration_delta = end - start
                        min = str(duration_delta).split(':')[1]
                        sec = str(duration_delta).split(':')[2]

                        if min[0] == '0':
                            min = min[1]
                        if sec[0] == '0':
                            sec = sec[1]

                        if min == '0':
                            duration = sec + ' seconds'
                        else:
                            if min == '1':
                                duration = min + ' minute and ' + sec + ' seconds'
                            else:
                                duration = min + ' minutes and ' + sec + ' seconds'

                    except:
                        print('blocco locations finito')

                    context.get('locations').append(
                        {'start': str(start).split()[1], 'end': str(end).split()[1], 'position': position,
                         'duration': duration, 'visitor': visitor, 'group': group, 'x': x, 'y': y})
"""




"""       
                avoid_events = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                with open(os.path.join('media/', file.name)) as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    prima_ = next(reader)
                    if next(reader)[0] in avoid:
                        next(reader)

                    for line in reader:
                        if line[0][0] not in avoid:
                            next(reader)

                         
                         
                        for elem in mappa:
                            print(elem.name)
                            if elem.name == str(position):
                                x = elem['x']
                                y = elem['y']
"""


