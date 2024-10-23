from django import forms
from products.models import Promo

class PromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        fields = ['promo_title', 'promo_description', 'price_before', 'price_after']