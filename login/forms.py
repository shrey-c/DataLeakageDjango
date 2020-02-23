from django import forms
from .models import LoginDetails

class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control',
            'placeholder':'username'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control',
            'placeholder':'password',
        }   
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
    	model = LoginDetails
    	fields = ('username', 'password')
class LoginDetailsForm(MyModelForm):
	form_class = MyModelForm
