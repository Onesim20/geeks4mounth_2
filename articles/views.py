from django.http.response import HttpResponse


def hello_world(request):
    return HttpResponse("asd")


def hello_name(request, name):
    return HttpResponse(f"Hello <h1>{name}</h1>!")

def User_age(request, age):
    return HttpResponse(f"Your age is <h1>{age}</h1>!")




# Create your views here.

