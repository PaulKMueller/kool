import json
from django.shortcuts import render
from competence_page.models import Category
import access


def categories_page(request):
    '''Render Category Page, which shows all the categories'''
    category_names = access.get_request_from_api("/all_categories")
    category_names.sort(key=lambda a: a[1])
    categories_obj = []
    print(category_names)
    for category in category_names:
        new_cat = Category()
        new_cat.name = category[1]
        new_cat.link = category[0]
        new_cat.img = "/static/images/" + str(category[0]) + ".jpg"
        categories_obj.append(new_cat)
    all_competencies = access.get_request_from_api("/all_competencies/")

    return render(request, 'competence_categories.html',
                  {'categories': categories_obj,
                   'all_competencies': json.dumps(all_competencies)})


def competence_page(request, id):
    '''Render Competency Page, which shows all the competencies to a given
    category id

            Parameters:
                    id (int): Category_id
    '''
    competencies = access.get_request_from_api("/competencies_by_category_id/"
                                               + str(id))
    competencies.sort(key=lambda a: a[1])
    name = access.get_request_from_api("/category_name/" + str(id))[0]
    all_competencies = access.get_request_from_api("/all_competencies/")
    return render(request, 'category.html',
                  {'name': name,
                   'competencies': competencies,
                   'all_competencies': json.dumps(all_competencies)})
