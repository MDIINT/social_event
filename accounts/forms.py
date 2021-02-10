from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import Profile, User
from eventing.models import Event


class RegisterForm(UserCreationForm):
    """
    client signup form
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserEdit(UserChangeForm):
    """
    users can change 'first name', 'last name', 'email'
    """
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'email']
    password = None


class ProfileEdit(forms.ModelForm):
    """
    users can change 'mobile', 'address, 'user type account', 'organ name', 'birth date' and 'profile image'
    """
    class Meta:
        model = Profile
        fields = ['mobile', 'address', 'user_type', 'organ_name', 'birth_date', 'profile_image']
        user_type_choices = Profile.user_type_choices


class CreatEvent(forms.ModelForm):
    """
    user create new own event
    """
    class Meta:
        model = Event
        fields = ['title', 'subject', 'details', 'tags', 'start_date', 'end_date', 'poster']


class EditEvent(forms.ModelForm):
    """
    user can edit own created event
    """
    class Meta:
        model = Event
        fields = ['title', 'subject', 'details', 'start_date', 'end_date', 'tags', 'poster', 'cancel']


class VerifyEvent(forms.ModelForm):
    """
    admin can verify and edit event
    """
    class Meta:
        model = Event
        fields = ['title', 'subject', 'details', 'start_date', 'end_date',
                  'tags', 'poster', 'cancel', 'verify']
