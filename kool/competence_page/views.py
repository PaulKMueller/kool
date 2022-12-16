from django.shortcuts import render
from competence_page.models import Category
import requests
import time
# Create your views here.

biology = Category()
biology.name = 'Biology'
biology.link = '/competence/123'
biology.img = 'https://cdn.pixabay.com/photo/2019/03/19/19/54/butterflies-4066785_960_720.jpg'
url = "http://localhost:8020/all_categories"

def categories_page(request):
    
    categories = get_request_from_api(url)

    category = Category()
    category.name = "categories"

    print(categories)
    return render(request, 'competence_categories.html',
                  {'categories': categories})


def get_request_from_api(url):
    for i in range(5):
        try:
            response = requests.get(url)
            return response.json()
        except:
            time.sleep(2)
            continue
    return "connection failed"

def competence_page(request, id):
    print(id)
    return render(request, 'category.html', {'name': id,
                                            'competencies': ["Machine Learning", "Linear Algebra", "Cocklecken", get_request_from_api(url)[0]]} )
