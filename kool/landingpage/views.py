import csv
from django.shortcuts import render
from django.http import HttpResponse


content = []

with open('/workspaces/kool/firsttest.csv', encoding='UTF-8') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        content.append([row[0], row[1]])


def home(request):
    return render(request, 'home.html', {'content':content})
