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
from django.urls import path

from articles.views import (
    article_create,
    article_delete,
    article_detail,
    article_edit,
    articles_list,
    category_list,
    comment_create,
    comment_delete,
    comment_edit,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("categories/", category_list),
    path("", articles_list, name="article_list"),
    path("<int:id>/detail", article_detail, name="article_detail"),
    path("<int:id>/edit", article_edit, name="article_edit"),
    path("<int:id>/delete", article_delete, name="article_delete"),
    path("create/", article_create, name="article_create"),
    path("<int:article_id>/comments/", comment_create, name="comment_create"),
    path("comments/<int:id>/edit", comment_edit, name="comment_edit"),
    path("comments/<int:id>/delete", comment_delete, name="comment_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)