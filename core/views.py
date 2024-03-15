from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'core/index.html')
