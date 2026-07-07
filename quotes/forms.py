from django import forms
from django.contrib.auth.forms import UserCreationForm
from .documents import Author, Quote


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class AuthorForm(forms.Form):
    fullname = forms.CharField(max_length=200)
    born_date = forms.CharField(max_length=50)
    born_location = forms.CharField(max_length=150)
    description = forms.CharField(widget=forms.Textarea)

class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=200)
    author = forms.ChoiceField(choices=[]) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].choices = [(a.fullname, a.fullname) for a in Author.objects.all()]