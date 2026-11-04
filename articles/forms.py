from django import forms

from articles.models import Article, Comment

# class ArticleForm(forms.Form):
#     title = forms.CharField(min_length=5, max_length=100)
#     text = forms.Textarea()
#     rate = forms.IntegerField(min_value=0, max_value=10)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "text", "rate", "image", "category")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author_name", "text")


