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
from django.db.utils import DataError
import logging

logger = logging.getLogger(__name__)

ENTRIES_COUNT = 20


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_log_entry(request, user, message):
    ip = get_client_ip(request)
    logger.error(f"| User: {user} | IP:{ip} | Message: {message}")


class IndexView(View):
    def get(self, request):
        return render(request, 'text/index.html')


@method_decorator(login_required, name='dispatch')
class CreateView(View):
    def get(self, request):
        form = forms.TextForm()
        return render(request, 'text/create.html', {'form': form})

    def post(self, request):
        form = forms.TextForm(request.POST)
        if form.is_valid():
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
        else:
            return render(request, 'text/create.html', {'form': form})



class DetailView(View):
    def get(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        tags = models.Tag.objects.filter(text = text)
        comments = models.Comment.objects.filter(text = text)
        return render(request, 'text/detail.html', {
            'text': text,
            'tags': tags,
            'comments': comments
            })


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
            add_log_entry(request, request.user, f"GET Попытка изменения кода с id={text.id}")
            return HttpResponseForbidden()

    def post(self, request, text_id):
        text = get_object_or_404(models.Text, id=text_id)
        tags_obj = models.Tag.objects.filter(text=text_id)
        for obj in tags_obj:
            obj.delete()
        if request.user == text.user:
            text.text = request.POST['textfield']
            text.topic = request.POST['topic']
            text.date_last_change = timezone.now()
            try:
                text.save()
            except DataError:
                error = 'Превышен лимит количества символов!'
                add_log_entry(request, request.user, "Превышен лимит количества символов")
                return render(request, 'text/edit.html', {'text': text,'error':error})
            tags = request.POST['tags']
            list_tags = tags.split(',')
            for tag in list_tags:
                tag_obj = models.Tag(tag = tag, text=text)
                tag_obj.save()
            return redirect('text:detail', text_id=text.id)
        else:
            add_log_entry(request, request.user, f"POST Попытка изменения кода с id={text.id}")
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
            add_log_entry(request, request.user, f"POST Попытка удаления кода с id={text.id}")
            return HttpResponseForbidden()


@method_decorator(login_required, name='dispatch')
class SearchByTagView(TemplateView):
    template_name = 'text/tagsearch.html'

    def get_context_data(self, tag):
        texts = models.Tag.objects.filter(tag = tag)
        return {'texts': texts, 'tag': tag}


class AllCodeView(View):
    def get(self, request):
        all_codes = models.Text.objects.all()
        paginator = Paginator(all_codes, ENTRIES_COUNT)
        page = request.GET.get('page')
        codes = paginator.get_page(page)
        return render(request, 'text/allcode.html', {'codes': codes})


class CreateCommentView(View):
    def post(self, request, text_id):
        text_obj = get_object_or_404(models.Text, id=text_id)
        form = forms.AddCommentForm(request.POST)
        if form.is_valid():
            comment = request.POST['comment']
            reply_to_id = request.POST['reply_to']
            comm_obj = models.Comment(commentary=comment, user=request.user, text=text_obj)
            if reply_to_id:
                reply_comment = get_object_or_404(models.Comment, id=reply_to_id)
                comm_obj.reply_to = reply_comment
            comm_obj.save()
            return redirect('text:detail', text_id=text_obj.id)
        else:
            text = get_object_or_404(models.Text, id=text_id)
            tags = models.Tag.objects.filter(text = text)
            comments = models.Comment.objects.filter(text = text)
            return render(request, 'text/detail.html', {
                'text': text,
                'tags': tags,
                'comments': comments,
                'form':form
                })

class UpdateCommentView(View):
    def post(self, request, comment_id, text_id):
        comm = get_object_or_404(models.Comment, id=comment_id)
        if request.user == comm.user:
            comm.comment = request.POST['comment']
            comm.save()
            return redirect('text:detail', text_id=text_id)
        else:
            add_log_entry(request, request.user, f"POST Попытка изменения комментария с id={comm.id}")
            return HttpResponseForbidden()

class DeleteCommentView(View):
    def post(self, request, comment_id, text_id):
        comm = get_object_or_404(models.Comment, id=comment_id)
        if request.user == comm.user:
            comm.delete()
            return redirect('text:detail', text_id=text_id)
        else:
            add_log_entry(request, request.user, f"POST Попытка удаления комментария с id={comm.id}")
            return HttpResponseForbidden()