from django.shortcuts import render


def adminpage(request):
    return render(request, 'admin.html')


def add_entries(request):
    return render(request, 'add_entries.html')
