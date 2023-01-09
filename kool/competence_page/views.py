from django.shortcuts import render
from competence_page.models import Category
import requests
import json
import time
import access

biology = Category()
biology.name = 'Biology'
biology.link = '/competence/123'
biology.img = 'https://cdn.pixabay.com/photo/2019/03/19/19/54/butterflies-4066785_960_720.jpg'


def categories_page(request):
    category_names = access.get_request_from_api("/all_categories")
    category_names.sort(key=lambda a: a[1])
    categories_obj = []
    print(category_names)
    for category in category_names:
        newCat = Category()
        newCat.name = category[1]
        newCat.link = category[0]
        newCat.img = "/static/images/" + str(category[0]) + ".jpg"
        categories_obj.append(newCat)
    all_competencies = access.get_request_from_api("/all_competencies/")
    
    return render(request, 'competence_categories.html',
                  {'categories': categories_obj, 'all_competencies': json.dumps(all_competencies)})

def competence_page(request, id):
    competencies = access.get_request_from_api("/competencies_by_category_id/" + str(id))
    competencies.sort(key=lambda a: a[1])
    name = access.get_request_from_api("/category_name/" + str(id))[0]
    all_competencies = access.get_request_from_api("/all_competencies/")
    
    return render(request, 'category.html', {'name': name,
                                             'competencies': competencies,
                                             'all_competencies': json.dumps(all_competencies)})
