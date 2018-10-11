from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from . import models
from django.core.paginator import Paginator
from . import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

ENTRIES_COUNT = 20


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        texts_list = models.Text.objects.filter(user=request.user)
        paginator = Paginator(texts_list, ENTRIES_COUNT)
        page = request.GET.get('page')
        texts = paginator.get_page(page)
        return render(request, 'text/index.html', {
            'texts': texts,
            'request': request
        })


@method_decorator(login_required, name='dispatch')
class CreateView(View):
    def get(self, request):
        form = forms.TextForm()
        return render(request, 'text/create.html', {'form': form})

    def post(self, request):
        text_post = request.POST['textfield']
        tags = request.POST['tags']
        topic = request.POST['topic']
        list_tags = tags.split(',')
        text_obj = models.Text(text=text_post, user=request.user, topic=topic)
        text_obj.save()
        for tag in list_tags:
            tag_obj = models.Tag(tag = tag, text=text_obj)
            tag_obj.save()
        return redirect('text:detail', text_id=text_obj.id)


@method_decorator(login_required, name='dispatch')
class DetailView(TemplateView):
    template_name = 'text/detail.html'

    def get_context_data(self, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        tags = models.Tag.objects.filter(text = text)
        return_url = self.request.GET.get('next')
        return {'text': text, 'url': return_url, 'tags': tags}


@method_decorator(login_required, name='dispatch')
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

    def post(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        tag_obj = get_object_or_404(models.Tag, text=text)
        if request.user == text.user:
            text.text = request.POST['textfield']
            text.topic = request.POST['topic']
            text.date_last_change = timezone.now()
            text.save()
            tags = request.POST['tags']
            list_tags = tags.split(',')
            for tag in list_tags:
                tag_obj.tag = tag
                tag_obj.save()
            return redirect('text:detail', text_id=text.id)
        else:
            return HttpResponseForbidden()


@method_decorator(login_required, name='dispatch')
class DeleteView(TemplateView):
    template_name = 'text/delete.html'

    def get_context_data(self, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        return_url = self.request.GET.get('next')
        if return_url == None:
            return_url = "/"
        return {'text': text, 'url': return_url}

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


@method_decorator(login_required, name='dispatch')
class SearchByTagView(TemplateView):
    template_name = 'text/tagsearch.html'

    def get_context_data(self, tag):
        texts = models.Tag.objects.filter(tag = tag)
        return {'texts': texts, 'tag': tag}