from django import forms
from .models import Order

PRODUCT_CHOICES = []
for i in range(1,6):
     PRODUCT_CHOICES.append((i,(str(i))))

class Select_Quantity_Form(forms.Form):
    select_quantity = forms.TypedChoiceField(choices=PRODUCT_CHOICES,coerce=int, label='', widget=forms.Select(attrs={'class':'form-select','style':'width:100%'}))

class Fill_Data_Form(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}))
    surname = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last name'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'E-mail'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}))
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    post_code = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post code'}))
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    
    class Meta:
        model = Order
        fields = ['name','surname','email','phone','address','post_code','city']

