from django.shortcuts import render
# from django.http import HttpResponse
# import pandas as pd
# from . import models


# content = []

def home(request):
    return render(request, 'home.html')

def aboutkoolpage(request):
    return render(request, 'aboutkool.html')


