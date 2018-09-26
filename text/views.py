from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView
from django.views import View
from . import models


class IndexView(TemplateView):
    template_name = 'text/index.html'

    def get_context_data(self):
        texts = models.Text.objects.all()
        return {'texts': texts}


class DetailView(TemplateView):
    template_name = 'text/detail.html'

    def get_context_data(self, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        return {'text': text}


class EditView(View):
    def get(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        if request.user == text.user:
            return render(request, 'text/edit.html', {'text': text})
        else:
            return HttpResponseForbidden()


class AddView(View):
    def post(self, request):
        text_post = request.POST['textfield']
        text_obj = models.Text(text=text_post, user=request.user)
        text_obj.save()
        return redirect('text:detail', text_id=text_obj.id)


class UpdView(View):
    def get(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        if request.user == text.user:
            text.text = request.POST['textfield']
            text.save()
            return redirect('text:detail', text_id=text.id)
        else:
            return HttpResponseForbidden()
