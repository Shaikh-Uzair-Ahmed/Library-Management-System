from django import forms

class BookRequestForm(forms.Form):
    title = forms.CharField(label="Book Title", max_length=100,required=False)
    author = forms.CharField(label="Author", max_length=100, required=False)
    isbn = forms.CharField(label="ISBN", min_length=13,max_length=13)



