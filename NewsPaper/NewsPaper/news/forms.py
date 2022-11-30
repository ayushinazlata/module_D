from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['publication',
                  'title',
                  'text',
                  'post_category',
                  ]

    def clean_name(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return title

