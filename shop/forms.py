""" Module defining the forms used in the application """
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categories, Images, Products

class CustomUserCreationForm(UserCreationForm):
    """ Form to create a new user """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class categoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description']

class combinedForm(forms.Form):
    name = forms.CharField(max_length=100)
    category = forms.ModelChoiceField(queryset=Categories.objects.all())
    price = forms.IntegerField()
    quantity = forms.IntegerField()
    description = forms.CharField(max_length=300)
    features = forms.CharField(max_length=300)
    image1_url = forms.ImageField()
    image2_url = forms.ImageField()
    image3_url = forms.ImageField()
    image4_url = forms.ImageField()
    image5_url = forms.ImageField()
