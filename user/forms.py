from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    user_info = forms.CharField(max_length=100, label='Username Or Email' ,widget=forms.TextInput)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    
    def clean(self):
        super().clean()
        user_info = self.cleaned_data.get('user_info')
        password = self.cleaned_data.get('password')
        if not user_info or not password:
            return

        user_instance = None
        if '@' in user_info:
            user_instance = User.objects.filter(email=user_info).first()
        else:
            user_instance = User.objects.filter(username=user_info).first()
        
        
        if not user_instance:
            raise forms.ValidationError('Bele bir user yoxdur!')
        
        self.user = None
        if user_instance.check_password(password):
            self.user = user_instance
        else:
            raise forms.ValidationError('Sifre yanlisdir!')

        


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    username = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError('Sifreler eyni deyil!')