from django import forms
from re import compile
from .models import Contact

name_compiler = compile('^[A-Z][a-z]{3,} [A-Z][a-z]{3,}$')
email_name_compiler = compile('^([\w]+)@')

# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=50, initial="Filankes Filankesov", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
#     email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
#     phone = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
#     message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}))

#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         email = cleaned_data.get('email')
#         email_name = email_name_compiler.search(email).groups()[0]
#         if email and name and  email_name.lower() in name.lower():
#             raise forms.ValidationError('Ad email daxilinde ola bilmez!')
        

#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if name and not name_compiler.search(name):
#             raise forms.ValidationError('Ad duzgun yazilmayib!')
#         return name
        
class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'})
        }