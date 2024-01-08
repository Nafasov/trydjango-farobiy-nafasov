from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'placeholder': 'title',
            'class': "form-control",
        })
        self.fields['image'].widget.attrs.update({
            'class': "form-control"
        })
        self.fields['content'].widget.attrs.update({
            'placeholder': 'content',
            'class': 'form-control',
            'cols': 60,
            'rows': 5,
        })


# from django import forms
# from django.core.exceptions import ValidationError
# from .models import Article
#
#
# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title', 'image', 'content']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs.update({
#             'placeholder': 'title',
#             'class': 'form-control mb-3',
#
#         })
#         self.fields['content'].widget.attrs.update({
#             'cols': 60,
#             'rows': 5,
#             'placeholder': 'content',
#             'class': 'form-control mb-3'
#         })
#         self.fields['image'].widget.attrs.update({
#             'class': 'form-control col-mb-3'
#         })
#         # self.fields['slug'].widget.attrs.update({
#         #     'class': 'form-control col-mb-3'
#         # })
#
#     def clean_title(self):
#         if self.cleaned_data['title'].replace(' ', '').isalnum():
#             return self.cleaned_data['title']
#         raise ValidationError('bunday title mumkin emas')
