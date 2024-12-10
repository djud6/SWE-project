from django import forms
from .models import Post, Comment, Club, Theme, BookRecommendation, BookDiscussion

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
    
    # Explicitly set `goodreads_url` as not required
    goodreads_url = forms.CharField(required=False)

# Add this to forms.py
class BookDiscussionForm(forms.ModelForm):
    class Meta:
        model = BookDiscussion
        fields = ['book_title', 'book_cover', 'goodreads_url', 'discussion_title', 'discussion_description']