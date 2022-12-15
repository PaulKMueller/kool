from django.shortcuts import render
from competence_page.models import Category
# Create your views here.

biology = Category()
biology.name = 'Biology'
biology.link = '/competence/biology'
biology.img = 'https://cdn.pixabay.com/photo/2019/03/19/19/54/butterflies-4066785_960_720.jpg'

chemistry = Category()
chemistry.name = 'Chemistry'
chemistry.link = '/competence/chemistry'
chemistry.img = 'https://cdn.pixabay.com/photo/2012/11/07/21/23/showcase-65306_960_720.jpg'

cs = Category()
cs.name = 'Computer_Science'
cs.link = '/competence/cs'
cs.img = 'https://cdn.pixabay.com/photo/2022/04/04/16/42/technology-7111799_960_720.jpg'

economics = Category()
economics.name = 'Economics'
economics.link = '/competence/economics'
economics.img = 'https://cdn.pixabay.com/photo/2016/10/09/19/19/coins-1726618_960_720.jpg'

categories = [biology, chemistry, cs, economics]


def categories_page(request):
    return render(request, 'competence_categories.html',
                  {'categories': categories})


def competence_page(request):
    return render(request, 'biology.html', {'name': 'Biology',
                                            'numbers': range(30)})
