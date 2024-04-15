from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_category', 'author', 'post_title', 'post_text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("post_title")
        text = cleaned_data.get("post_text")

        if title == text:
            raise ValidationError(
                "Заголовок не должен быть идентичен содержанию."
            )

        return cleaned_data