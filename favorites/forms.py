from django import forms
from .models import Favorite

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['category']
    
    category = forms.ChoiceField(
        choices=Favorite.Category.choices,
        widget=forms.Select()
    )