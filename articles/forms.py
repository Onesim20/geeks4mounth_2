import re

from django import forms

from articles.models import Article, Comment

# class ArticleForm(forms.Form):
#     title = forms.CharField(min_length=5, max_length=100)
#     text = forms.Textarea()
#     rate = forms.IntegerField(min_value=0, max_value=10)


FORBIDDEN_WORDS = ("baaaaaaka", "spam", "дурак", "идиот", "тупица", "казино", "scam")


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "text", "rate", "image", "category")
        
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "rate": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    
    def validation_title(self, title):
        if len(title) > 10:
            raise forms.ValidationError("validation error from func")

    
    def clean_title(self):
        title = self.cleaned_data["title"]

        if title == "NOT VALID":
            raise forms.ValidationError("TUT")

        self.validation_title(title)

        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author_name", "text")
        widgets = {
            "author_name": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    
    def clean_author_name(self):
        author_name = self.cleaned_data["author_name"].strip()

        if author_name.replace(" ", "").isdigit():
            raise forms.ValidationError("Имя не может состоять только из цифр.")

        return author_name

    
    def clean_text(self):
        text = self.cleaned_data["text"].strip()

        if len(text) < 5:
            raise forms.ValidationError("Комментарий слишком короткий: минимум 5 символов.")

        
        words = re.findall(r"\w+", text.lower())
        found = [word for word in FORBIDDEN_WORDS if word in words]

        if found:
            raise forms.ValidationError("Запрещённые слова: " + ", ".join(found) + ".")

        return text