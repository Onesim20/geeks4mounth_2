"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from articles.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    CategoryListView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    MyArticlesListView,
    MyCommentsListView,
    SignUpView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("", ArticleListView.as_view(), name="article_list"),
    path("my", MyArticlesListView.as_view(), name="my_articles"),
    path("my-comments", MyCommentsListView.as_view(), name="my_comments"),
    path("<int:id>/detail", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:id>/edit", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:id>/delete", ArticleDeleteView.as_view(), name="article_delete"),
    path("create/", ArticleCreateView.as_view(), name="article_create"),
    path("<int:article_id>/comments/", CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:id>/edit", CommentUpdateView.as_view(), name="comment_edit"),
    path("comments/<int:id>/delete", CommentDeleteView.as_view(), name="comment_delete"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)