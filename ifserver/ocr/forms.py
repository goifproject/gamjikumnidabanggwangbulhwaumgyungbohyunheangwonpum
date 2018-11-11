from django import forms


class UploadFileForm(forms.Form):
    image = forms.ImageField()


class Base64Form(forms.Form):
    image = forms.ImageField()
