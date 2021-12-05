from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from store.models import Customer

def Register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            user = authenticate(username=username,password=password)
            Customer.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('index')

    else:
        f = UserCreationForm()

    template = "registration/register.html"
    return render(request, template, {'form': f})