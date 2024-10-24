from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']  # Assuming your review model has 'content' and 'rating'
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Write your review...'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'})
        }
