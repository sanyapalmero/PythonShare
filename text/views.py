from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from . import models
from django.core.paginator import Paginator
from . import forms

ENTRIES_COUNT = 20


class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'text/index.html', {
                'request': request
            })
        texts_list = models.Text.objects.filter(user=request.user)
        paginator = Paginator(texts_list, ENTRIES_COUNT)
        page = request.GET.get('page')
        texts = paginator.get_page(page)
        return render(request, 'text/index.html', {
            'texts': texts,
            'request': request
        })



class CreateView(View):
    def get(self, request):
        form = forms.TextForm()
        return render(request, 'text/create.html', {'form': form})


class DetailView(TemplateView):
    template_name = 'text/detail.html'

    def get_context_data(self, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        return_url = self.request.GET.get('next')
        return {'text': text, 'url': return_url}


class EditView(View):
    def get(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        if request.user == text.user:
            form = forms.TextForm()
            return render(request, 'text/edit.html', {
                'text': text,
                'form': form
            })
        else:
            return HttpResponseForbidden()


class DeleteView(TemplateView):
    template_name = 'text/delete.html'

    def get_context_data(self, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        return_url = self.request.GET.get('next')
        if return_url == None:
            return_url = "/"
        return {'text': text, 'url': return_url}


class DelView(View):
    def post(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        if request.user == text.user:
            return_url = request.POST['next']
            if return_url == 'None':
                return_url = "/"
            text.delete()
            return HttpResponseRedirect(return_url)
        else:
            return HttpResponseForbidden()

    def get(self, request, text_id):
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
