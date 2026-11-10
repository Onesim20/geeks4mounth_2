from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment


def article_comments_url(article_id: int) -> str:
    return reverse("article_detail", args=[article_id]) + "#comments"


def articles_list(request: HttpRequest) -> HttpResponse:
    articles_list = Article.objects.all()

    return render(request, "articles/list.html", {"articles": articles_list})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    form = CommentForm()
    comments = article.comment_set.all()
    return render(
        request,
        "articles/detail.html",
        {"article": article, "form": form, "comments": comments},
    )


def comment_create(request: HttpRequest, article_id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=article_id)

    if request.method != "POST":
        return redirect("article_detail", id=article_id)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        return redirect(article_comments_url(article_id))

    return render(
        request,
        "articles/detail.html",
        {"article": article, "form": form, "comments": article.comment_set.all()},
    )


def comment_edit(request: HttpRequest, id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, id=id)
    form = CommentForm(request.POST or None, instance=comment)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(article_comments_url(comment.article_id))

    return render(request, "articles/comment_edit.html", {"form": form, "comment": comment})


def comment_delete(request: HttpRequest, id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, id=id)

    if request.method == "POST":
        article_id = comment.article_id
        comment.delete()
        return redirect(article_comments_url(article_id))

    return render(request, "articles/comment_delete.html", {"comment": comment})


def article_create(request: HttpRequest) -> HttpResponse:
    form = ArticleForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_list")

    return render(request, "articles/create.html", {"form": form})


def article_edit(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=form.instance.id)

    return render(request, "articles/edit.html", {"form": form})


def article_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if request.method == "POST":
        article.delete()
        return redirect("article_list")

    return render(request, "articles/delete.html", context={"article": article})


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