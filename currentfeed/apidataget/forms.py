from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import ModelForm
from apidataget.models import Save

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    first_name = forms.CharField(label='Enter First Name', min_length=4, max_length=150)
    last_name=forms.CharField(label='Enter Last Name',min_length=4,max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        user=self.cleaned_data['username']
        try:
            match=User.objects.get(username=user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError(' This username already exist')

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            mt=validate_email(email)
        except:
            return forms.ValidationError("Email is not in correct format")
        return email

    def clean_password2(self):
        pas=self.cleaned_data['password1']
        cpas=self.cleaned_data['password2']
        MIN_LENGTH=8
        if pas and cpas:
            if pas!=cpas:
                raise forms.ValidationError("Password and Confirm Password not matched")
            else:
                if len(pas)< MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast 8 characters")
                if pas.isdigit():
                    raise forms.ValidationError("Password should not be all numeric")
        return cpas


    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )

        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.save()
        return user

class ArticleForm(ModelForm):
    class Meta:
        model=Save
        fields=('article_title', 'article_description', 'article_image', 'article_url')
