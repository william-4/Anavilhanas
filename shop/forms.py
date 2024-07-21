""" Module defining the forms used in the application """
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Categories, Addresses, customUser, Images, Products

class customUserCreationForm(UserCreationForm):
    class Meta:
        model = customUser
        fields = ('first_name', 'last_name', 'email', 'city', 'phone_number', 'date_of_birth', 'password1', 'password2', )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class customUserEditForm(UserCreationForm):
    class Meta:
        model = customUser
        fields = ('first_name', 'last_name', 'email', 'city', 'phone_number', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class categoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description']

class addressesForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ['city', 'town', 'location', 'major_road', 'description']

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
