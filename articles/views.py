import math
from functools import cached_property
from typing import Any

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment


def article_comments_url(article_id: int) -> str:
    return reverse("article_detail", args=[article_id]) + "#comments"


def parse_rate(value: str) -> float | None:
    try:
        rate = float(value)
    except ValueError:
        return None
    return rate if math.isfinite(rate) else None


def parse_id(value: str) -> int | None:
    return int(value) if value.isdecimal() and len(value) <= 18 else None


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    denied_message = "Это не ваш объект"

    def test_func(self) -> bool:
        return self.get_object().user == self.request.user

    def get_denied_url(self) -> str:
        raise NotImplementedError

    def handle_no_permission(self) -> HttpResponse:
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, self.denied_message)
        return redirect(self.get_denied_url())


class ArticleOwnerMixin(OwnerRequiredMixin):
    model = Article
    pk_url_kwarg = "id"
    denied_message = "Это не ваш пост!"

    def get_denied_url(self) -> str:
        return self.get_object().get_absolute_url()


class CommentOwnerMixin(OwnerRequiredMixin):
    model = Comment
    pk_url_kwarg = "id"
    denied_message = "Это не ваш комментарий"

    def get_denied_url(self) -> str:
        return article_comments_url(self.get_object().article_id)

    def get_success_url(self) -> str:
        return article_comments_url(self.object.article_id)


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        context["users"] = User.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Article]:
        qs = super().get_queryset()
        params = self.request.GET

        if search := params.get("q"):
            qs = qs.filter(Q(title__icontains=search) | Q(text__icontains=search))

        if (rate := parse_rate(params.get("rate", ""))) is not None:
            if params.get("sort") == "gt":
                qs = qs.filter(rate__gte=math.ceil(rate))
            else:
                qs = qs.filter(rate__lte=math.floor(rate))

        if (category_id := parse_id(params.get("category", ""))) is not None:
            qs = qs.filter(category=category_id)

        if authors := [a for a in map(parse_id, params.getlist("users")) if a is not None]:
            qs = qs.filter(user_id__in=authors)

        return qs


class MyArticlesListView(LoginRequiredMixin, ArticleListView):
    def get_queryset(self) -> QuerySet[Article]:
        return super().get_queryset().filter(user=self.request.user)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comment_set.all()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = "articles/create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(ArticleOwnerMixin, UpdateView):
    form_class = ArticleForm
    template_name = "articles/edit.html"


class ArticleDeleteView(ArticleOwnerMixin, DeleteView):
    template_name = "articles/delete.html"
    success_url = reverse_lazy("article_list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = "articles/detail.html"

    @cached_property
    def article(self) -> Article:
        return get_object_or_404(Article, id=self.kwargs["article_id"])

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return redirect(self.article)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["article"] = self.article
        context["comments"] = self.article.comment_set.all()
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.article = self.article
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return article_comments_url(self.article.pk)


class CommentUpdateView(CommentOwnerMixin, UpdateView):
    form_class = CommentForm
    template_name = "articles/comment_edit.html"


class CommentDeleteView(CommentOwnerMixin, DeleteView):
    template_name = "articles/comment_delete.html"


class MyCommentsListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "articles/my_comments.html"
    context_object_name = "comments"

    def get_queryset(self) -> QuerySet[Comment]:
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .select_related("article")
            .order_by("-created_at")
        )


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("article_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("article_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Добро пожаловать! Аккаунт создан.")
        return response


class CategoryListView(ListView):
    model = Category































# Create your views here.

# def hello_world(request):
#     age = 1
#     return HttpResponse(f"Your age is {age}")


# def hello_name(request, name):
#     return HttpResponse(f"Hello <h1>{name}</h1>!")

# def User_age(request, age):
#     return HttpResponse(f"Your age is <h1>{age}</h1>!")