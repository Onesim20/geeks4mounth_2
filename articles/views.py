from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment




def articles_list(request: HttpRequest) -> HttpResponse:
    articles_list = Article.objects.all()

    return render(request, "articles/list.html", {"articles": articles_list})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    form = CommentForm()
    comments = article.comment_set.all()
    return render(request, "articles/detail.html", {"article": article, "form": form, "comments": comments})


def comment_create(request: HttpRequest, article_id: int) -> HttpResponse:
    article = Article.objects.get(id=article_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if not form.is_valid():
          commit = False
          comment = form.save(commit=False)
          comment.article = article
          comment.save()

        return redirect("article_detail", id=article_id)


def article_create(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if not form.is_valid():
            raise ValueError()
        form.save()
        return redirect("article_list")
    categories = Category.objects.all()
    return render(request, "articles/create.html", {"categories": categories})
    




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