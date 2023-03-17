from django import forms
from main.models import *

class Module2QForm(forms.Form):
	answer1 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
	answer2 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
class Module3QForm(forms.Form):
	answer1 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
	answer2 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
	answer3 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
class Module4QForm(forms.Form):
	answer1 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
	answer2 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
	answer3 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')
	answer4 = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15}), label='')