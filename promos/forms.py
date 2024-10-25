from django import forms
from promos.models import Promo

class PromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        fields = ['promo_title', 'promo_description', 'batas_penggunaan']
        widgets = {
            'promo_title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'promo_description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded'}),
            'batas_penggunaan': forms.DateInput(attrs={'class': 'w-full p-2 border rounded', 'type': 'date'}),
        }