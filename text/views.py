from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . import models


def index(request):
    return render(request, 'text/index.html')


def add(request):
    text_post = request.POST['textfield']
    text_obj = models.Text(text=text_post)
    text_obj.save()
    return redirect('text:detail', text_id=text_obj.id)


def detail(request, text_id):
    text = get_object_or_404(models.Text, id=text_id)
    return render(request, 'text/detail.html', {'text': text})
