from django.shortcuts import render

def results(request):
    return render(request, 'result_page.html')
