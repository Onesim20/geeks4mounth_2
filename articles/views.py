from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from articles.models import Article, Category



from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from articles.models import Article


def articles_list(request: HttpRequest) -> HttpResponse:
    articles_list = Article.objects.all()

    return render(request, "articles/list.html", {"articles": articles_list})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    return render(request, "articles/detail.html", {"article": article})








def category_list(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    text = "<h1>Categories:</h1><br>"

    for category in categories:
        text += f"<h2>{category.name}</h2><br>"
    return HttpResponse(text)





# Create your views here.

# def hello_world(request):
#     age = 1
#     return HttpResponse(f"Your age is {age}")


# def hello_name(request, name):
#     return HttpResponse(f"Hello <h1>{name}</h1>!")

# def User_age(request, age):
#     return HttpResponse(f"Your age is <h1>{age}</h1>!")