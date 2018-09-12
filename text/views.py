from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
# Create your views here.

def index(request):
    return render(request, 'text/index.html')

def add(request):
    text_post = request.POST['textfield']
    text_obj = models.Text(text = text_post)
    text_obj.save()
    return redirect('../../text/')



