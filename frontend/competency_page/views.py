import json

from django.shortcuts import render
from django.http import HttpRequest
from django.http.response import HttpResponse

from competency_page.models import Category
import access


def get_categories() -> list:
    """Gets all categories from backend and builds objects containing
    corresponding images and links

    Returns:
        list: List of all categories
    """
    category_names = access.get_request_from_api("/all_categories")
    category_names.sort(key=lambda a: a[1])
    categories_obj = []
    for category in category_names:
        category_object = Category()
        category_object.name = category[1]
        category_object.link = category[0]
        category_object.img = "/static/images/" + str(category[0]) + ".jpg"
        categories_obj.append(category_object)
    return categories_obj


def categories_page(request: HttpRequest) -> HttpResponse:
    """Render Category Page, which shows all the categories

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered categories page.
    """
    categories_obj = get_categories()
    all_competencies = access.get_request_from_api("/all_competencies/")

    return render(request, 'competency_categories.html',
                  {'categories': categories_obj,
                   'all_competencies': json.dumps(all_competencies)})


def competency_page(request: HttpRequest, id: int) -> HttpResponse:
    """Render Competency Page, which shows all the competencies to a given
    category id

    Args:
        request (HttpRequest): The request object.
        id (int): Category_id

    Returns:
        HttpResponse: The rendered competency page.
    """
    competencies = access.get_request_from_api("/competencies_by_category_id/"
                                               + str(id))
    competencies.sort(key=lambda a: a[1])
    name = access.get_request_from_api("/category_name/" + str(id))[0]
    all_competencies = access.get_request_from_api("/all_competencies/")
    return render(request, 'category.html',
                  {'name': name,
                   'competencies': competencies,
                   'all_competencies': json.dumps(all_competencies)})
