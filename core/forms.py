from django import forms
from django.contrib.auth.models import User
from .models import Profile, Application,Job

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type']  # Add more fields as needed
class JobForm(forms.ModelForm):
    class Meta:
        model= Job
        fields=['title','description','location','salary','category']

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
    



     