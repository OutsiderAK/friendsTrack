from django import forms
from django.core.validators import EmailValidator
from proj_twit.models import User


class LoginForm(forms.Form):
    login = forms.CharField(label='Your login')
    password = forms.CharField(widget=forms.PasswordInput(), label='Your password')


class AddPostForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'style': 'overflow: hidden; vertical-align: top;' 'resize: none;', 'rows': 5,
                   'placeholder': 'Max 200 characters'}),
        label='Message to users', max_length=200)


class RegisterUserForm(forms.Form):
    username = forms.CharField(label='Your nickname')
    email = forms.EmailField(widget=forms.EmailInput, validators=[EmailValidator])
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput, label='Repeat password')
    first_name = forms.CharField()
    last_name = forms.CharField()


class AddCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'overflow: hidden; vertical-align: top;' 'resize: none;', 'rows': 5,
               'placeholder': 'Max 200 characters'}),
        label='Comment this post', max_length=200)


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'overflow: hidden; vertical-align: top;' 'resize: none;', 'rows': 5,
               'placeholder': 'Max 500 characters'}),
        label='Message', max_length=200)
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
