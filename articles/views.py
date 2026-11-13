from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment


def article_comments_url(article_id: int) -> str:
    return reverse("article_detail", args=[article_id]) + "#comments"


def articles_list(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter()

    if search := request.GET.get("q"):
        articles = articles.filter(title__icontains=search)

    return render(request, "articles/list.html", {"articles": articles})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=id)
    form = CommentForm()
    comments = article.comment_set.all()
    return render(
        request,
        "articles/detail.html",
        {"article": article, "form": form, "comments": comments},
    )


@login_required
def comment_create(request: HttpRequest, article_id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=article_id)

    if request.method != "POST":
        return redirect("article_detail", id=article_id)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect(article_comments_url(article_id))

    return render(
        request,
        "articles/detail.html",
        {"article": article, "form": form, "comments": article.comment_set.all()},
    )


@login_required
def comment_edit(request: HttpRequest, id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, id=id)

    if comment.user != request.user:
        messages.error(request, "Это не ваш комментарий")
        return redirect(article_comments_url(comment.article_id))
    form = CommentForm(request.POST or None, instance=comment)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(article_comments_url(comment.article_id))

    return render(request, "articles/comment_edit.html", {"form": form, "comment": comment})


@login_required
def comment_delete(request: HttpRequest, id: int) -> HttpResponse:
    comment = get_object_or_404(Comment, id=id)

    if comment.user != request.user:
        messages.error(request, "Это не ваш комментарий")
        return redirect(article_comments_url(comment.article_id))

    if request.method == "POST":
        article_id = comment.article_id
        comment.delete()
        return redirect(article_comments_url(article_id))

    return render(request, "articles/comment_delete.html", {"comment": comment})


@login_required
def my_comments(request: HttpRequest) -> HttpResponse:
    comments = (
        Comment.objects.filter(user=request.user)
        .select_related("article")
        .order_by("-created_at")
    )
    return render(request, "articles/my_comments.html", {"comments": comments})


@login_required
def article_create(request: HttpRequest) -> HttpResponse:
    form = ArticleForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect("article_list")

    return render(request, "articles/create.html", {"form": form})


@login_required
def article_edit(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if article.user != request.user:
        messages.error(request, "Это не ваш пост!")
        return redirect("article_detail", id=article.pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=form.instance.id)

    return render(request, "articles/edit.html", {"form": form})


@login_required
def article_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if article.user != request.user:
        messages.error(request, "Это не ваш пост!")
        return redirect("article_detail", id=article.pk)

    if request.method == "POST":
        article.delete()
        return redirect("article_list")

    return render(request, "articles/delete.html", context={"article": article})


def signup(request):
    if request.user.is_authenticated:
        return redirect("article_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать! Аккаунт создан.")
            return redirect("article_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def my_articles(request: HttpRequest):
    articles = Article.objects.filter(user=request.user)
    return render(request, "articles/list.html", {"articles": articles})


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