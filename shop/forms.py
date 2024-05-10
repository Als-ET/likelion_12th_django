from django import forms
from .models import Item

class ItemForm(forms.Form):
    name = forms.CharField()
    count = forms.IntegerField()
    price = forms.IntegerField()
    store = forms.CharField()
    image = forms.ImageField()

class ItemModelForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
