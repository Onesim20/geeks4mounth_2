from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(null=True, upload_to="articles/")
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("-created_at",)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment by {self.user.username} on {self.article.title}"
    







































    


#CRUD - Create, Read, Update, Delete

# INSERT INTO table_name  (fields) Va


# num_1 = Article(title="title_1", text="This is my first article", rate=5)
# num_1.save()
# ###########
# num_2 =Article.objects.create(title="title_2", text="This is my second article", rate=4)
# #R
# articles = Article.objects.get(id=1)

# #D

# # 
# articles.delete()