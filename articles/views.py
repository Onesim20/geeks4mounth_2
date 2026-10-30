from django.http.request import HttpRequest
from django.http.response import HttpResponse

from articles.models import Article, Catalog

def hello_world(request):
    return HttpResponse("asd")


def hello_name(request, name):
    return HttpResponse(f"Hello <h1>{name}</h1>!")

def articles_list(request: HttpRequest) -> HttpResponse:
    count: int = Article.objects.all().count()
    text = "<h1>"
    for i in range(1, count + 1):
        article = Article.objects.filter(id=i).first()
        text += f"{article.title} </h1><br><h1>"
    return HttpResponse(text)

def catalog_list(request: HttpRequest) -> HttpResponse:
    catalogs = Catalog.objects.all()
    text = "<h1>Catalogs:</h1><br>"

    for dog in catalogs:
        text += f"<h2>{dog.name}</h2><br>"
    return HttpResponse(text)





# Create your views here.

# def hello_world(request):
#     age = 1
#     return HttpResponse(f"Your age is {age}")


# def hello_name(request, name):
#     return HttpResponse(f"Hello <h1>{name}</h1>!")

# def User_age(request, age):
#     return HttpResponse(f"Your age is <h1>{age}</h1>!")