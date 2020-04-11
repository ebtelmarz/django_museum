import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
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
    return render(request, 'museum/statistics.html')


def map(request):
    context = {
        'pos': Location.objects.all()
    }

    print(context)

    return render(request, 'museum/map.html', context)


def home(request):
    context = {
        'locations': [],
        # 'mappa': mappa
        # 'mappa': Location.objects.all()
    }

    mappa = Location.objects.all()

    x = 0
    y = 0

    if request.method == 'POST':
        key = 'document'
        if key not in request.FILES:
            messages.warning(request, f'Please upload a log file')
        else:
            file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(file.name, file)
            context['url'] = fs.url(name)

            visitor = file.name.split('.')[0].split('_')[1]
            group = file.name.split('.')[0].split('_')[2]

            avoid = ['e', 'p', 'P', 'E']

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
                        if line[0][0] in avoid:
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

            return render(request, 'museum/map.html', context)
    return render(request, 'museum/home.html', context)


# return redirect('museum-home')


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
