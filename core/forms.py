from django import forms
from .models import ProductReview


class ReviewForm(forms.ModelForm):

    RATING = (
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

    rating = forms.ChoiceField(choices=RATING, widget=forms.Select(attrs={
        'class': 'form-select m-2 p-2',
    }))

    review = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control m-2 p-2',
        'placeholder': 'Write your Review here...'
    }))

    # rating = forms.IntegerField(widget=forms.Select(
    #     attrs={'class': 'form-select m-2 p-2',
    #            'placeholder': 'Select Rating', }), choices=RATING)
