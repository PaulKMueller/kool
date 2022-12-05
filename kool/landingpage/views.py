from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from . import models


content = []

csvreader = pd.read_csv('/workspaces/kool/firsttest.csv', encoding='UTF-8', header=None)

#iterating through csv file using pandas
for expert, trustworthiness in zip(csvreader[0], csvreader[1]):
    content.append([expert, trustworthiness])


def home(request):
    return render(request, 'home.html', {'content':content})

