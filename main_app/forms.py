from django import forms
from .models import Entry#, Comment


class EntryForm(forms.ModelForm):

    class Meta:
        model=Entry
        fields=('title','short_desc','text')

# class CommentForm(forms.ModelForm):
#
#     class Meta:
#         model=Comment
#         fields=('text',)
