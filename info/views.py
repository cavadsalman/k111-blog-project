from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
    form = ContactForm(initial={'message': 'Menimle elaqe saxla'})
    return render(request, 'contact.html', context={'form': form})

        

def confirm_contact(request):
    if request.method == 'GET':
        return redirect('info:contact')
    elif request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('info:contact')
        return render(request, 'contact.html', context={'form': form})
    
    
def example(request):

    context = {
        'fruits': ['alma', 'armud', 'heyva', 'nar', 'saftali', 'gilas', 'albali', 'alca'],
        'star_value': 3.5
    }
    
    return render(request, 'example.html', context=context)