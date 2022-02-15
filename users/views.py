from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from users.forms import CustomUserCreationForm
from .forms import CustomUserCreationForm

def register(request):
    '''Register a new user'''
    if request.method != 'POST':
        # display empty form
        form = CustomUserCreationForm()
    else:
        # proccess filled form
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('budget:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)