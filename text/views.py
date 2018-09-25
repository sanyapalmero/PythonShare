from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from . import models


def index(request):
    texts = models.Text.objects.all()
    return render(request, 'text/index.html', {'texts': texts})


def add(request):
    text_post = request.POST['textfield']
    text_obj = models.Text(text=text_post, user=request.user)
    text_obj.save()
    return redirect('text:detail', text_id=text_obj.id)


def detail(request, text_id):
    text = get_object_or_404(models.Text, id=text_id)
    return render(request, 'text/detail.html', {'text': text})


def upd(request, text_id):
    text = get_object_or_404(models.Text, id=text_id)
    try:
        text.text = request.POST['textfield']
        text.save()
        return redirect('text:detail', text_id=text.id)
    except KeyError:
        return HttpResponseForbidden()


def edit(request, text_id):
    if request.user.is_authenticated:
        text = get_object_or_404(models.Text, id=text_id)
        return render(request, 'text/edit.html', {'text': text})
    else:
        return HttpResponseForbidden()
