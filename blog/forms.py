from django import forms


class AccessCodeForm(forms.Form):
    code = forms.CharField(max_length=20, label="Enter Access Code")
