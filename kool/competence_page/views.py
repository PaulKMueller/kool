from django.shortcuts import render

# Create your views here.


def competence_page(request):
    return render(request, 'competence_categories.html')


def cs_page(request):
    return render(request, 'computer_science.html')
