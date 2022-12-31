from django import forms
from django.forms import widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','desc']


class DateInput(forms.DateInput):
    input_type = 'date'
        
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','desc','due','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label='Nhập vào từ khóa')

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class ConversionForm(forms.Form):
    _choices = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices = _choices, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    _choices = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Nhập vào số cần chyển đổi'}
    ))
    measure1 = forms.CharField(
        label='',widget=forms.Select( choices= _choices)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select( choices= _choices)
    )

class ConversionMassForm(forms.Form):
    _choices = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Nhập vào số cần chyển đổi'}
    ))
    measure1 = forms.CharField(
        label='',widget=forms.Select( choices= _choices)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select( choices= _choices)
    )
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']