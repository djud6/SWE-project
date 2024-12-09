from django import forms
from django.contrib.auth.forms import UserCreationForm
from discussion.models import User,Profile, Theme


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['fname', 'lname', 'username', 'email', 'password1', 'password2']
        labels = { 'fname': 'First Name', 'lname': 'Last Name', }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'goodreads_url']

class ThemeSelectionForm(forms.Form):
    themes = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

class BooksPerYearForm(forms.Form):
    choices = [
        ('0-5', '0-5'),
        ('5-10', '5-10'),
        ('10-20', '10-20'),
        ('20+', '20+')
    ]
    books_per_year = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)



class UserProfileEditForm(forms.ModelForm):
    # Fields from the User model
    fname = forms.CharField(max_length=200, required=False, label="First Name")
    lname = forms.CharField(max_length=200, required=False, label="Last Name")
    username = forms.CharField(max_length=150, required=True, label="Username")

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'goodreads_url']  # Fields from Profile

    def __init__(self, *args, **kwargs):
        # Retrieve the user instance from kwargs
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        # Populate initial values for User fields
        if self.user_instance:
            self.fields['fname'].initial = self.user_instance.fname
            self.fields['lname'].initial = self.user_instance.lname
            self.fields['username'].initial = self.user_instance.username

    def save(self, commit=True):
        # Save Profile fields
        profile = super().save(commit=False)

        # Save User fields
        if self.user_instance:
            self.user_instance.fname = self.cleaned_data['fname']
            self.user_instance.lname = self.cleaned_data['lname']
            self.user_instance.username = self.cleaned_data['username']
            if commit:
                self.user_instance.save()

        if commit:
            profile.save()

        return profile
