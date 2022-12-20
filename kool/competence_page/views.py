from django.shortcuts import render
from competence_page.models import Category
import requests
import time
# Create your views here.

biology = Category()
biology.name = 'Biology'
biology.link = '/competence/123'
biology.img = 'https://cdn.pixabay.com/photo/2019/03/19/19/54/butterflies-4066785_960_720.jpg'
main_url = "http://192.168.123.116:8020"
url = "http://192.168.123.116:8020/all_categories"


def categories_page(request):
    category_names = get_request_from_api(url)
    category_names.sort(key=lambda a: a[1])
    categories_obj = []
    print(category_names)
    for category in category_names:
        newCat = Category()
        newCat.name = category[1]
        newCat.link = category[0]
        newCat.img = "/static/images/" + str(category[0]) + ".jpg"
        categories_obj.append(newCat)

    return render(request, 'competence_categories.html',
                  {'categories': categories_obj})


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
    competencies_req_url = main_url + "/competencies_by_category_id/" + str(id)
    name_req_url = main_url + "/category_name/" + str(id)

    competencies = get_request_from_api(competencies_req_url)
    competencies.sort(key=lambda a: a[1])

    name = get_request_from_api(name_req_url)[0]
    return render(request, 'category.html', {'name': name,
                                             'competencies': competencies})
