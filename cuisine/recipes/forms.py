from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'placeholder': 'Введите комментарий',
                                                 'cols': 60,
                                                 'rows': 5})}
        labels = {'body': ''}


class SearchForm(forms.Form):
    query = forms.CharField()
