from django import forms
from .models import Post, Comment, Club, Theme, BookRecommendation

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ClubForm(forms.ModelForm):
    theme = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use a checkbox select if you want multiple selections
        required=False  # Make it optional
    )
    class Meta:
        model = Club
        fields = ['name', 'description','theme']

class BookRecommendationForm(forms.ModelForm):
    class Meta:
        model = BookRecommendation
        fields = ['title', 'goodreads_url', 'cover_image', 'description']

