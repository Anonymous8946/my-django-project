from itertools import product
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class SubProduct(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,                         # Delete products if related subproduct is deleted
        null=False,
        blank=True 
        ,default='')

    def __str__(self):
        return self.name

class MainProduct(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    image2 = models.ImageField(upload_to='flowerorde/png', blank=True, null=True)  # Optional second image
    image3 = models.ImageField(upload_to='flowerorde/png', blank=True, null=True)  # Optional third image
    video = models.FileField(upload_to='flowerorde/videos', blank=True, null=True)  # Optional video file
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class MainSubProduct(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    mainproduct = models.ForeignKey(
        MainProduct,
        on_delete=models.CASCADE,                         # Delete products if related subproduct is deleted
        null=False,
        blank=True 
        ,default='')

    def __str__(self):
        return self.name
    
class LastProduct(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class SubLastProduct(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    lastProduct = models.ForeignKey(
        LastProduct,
        on_delete=models.CASCADE,                         # Delete products if related subproduct is deleted
        null=False,
        blank=True 
        ,default='')

    def __str__(self):
        return self.name
    
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={'exists': 'This email already exists.'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        # Add attributes for widgets
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'input-with-icon',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'E-mail',
            'class': 'input-with-icon',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'input-with-icon',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'input-with-icon',
        })

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user  # Return the saved user instance

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.fields['email'].error_messages['exists']
            )
        return email  # Return the validated email field value

class Order(models.Model):
    image = models.ImageField(upload_to= 'flowerorde/png')
    product = models.CharField(max_length=100,default='')
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=1000,default='')
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode  = models.CharField(max_length=10)
   
    date = models.DateField(default=datetime.datetime.today)
    
    def __str__(self):
        return self.product


