import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.utils import DataError
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from . import forms, models

logger = logging.getLogger(__name__)

ENTRIES_COUNT = 20 # Количество строк в таблице

# Метод get_client_ip возвращает ip адрес пользователя
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Метод add_log_entry добавляет строку об ошибке в файл error.log
def add_log_entry(request, user, message):
    ip = get_client_ip(request)
    logger.error(f"| User: {user} | IP:{ip} | Message: {message}")


# Класс Index, содержащий get метод, который возвращает страницу index.html
class IndexView(View):
    def get(self, request):
        return render(request, 'code/index.html')


# Класс Сreate
@method_decorator(login_required, name='dispatch')
class CreateView(View):
    # метод get, возвращающий страницу create.html
    def get(self, request):
        form = forms.CodeForm()
        return render(request, 'code/create.html', {'form': form})

    # метод post, отвечающий за добавление кода
    def post(self, request):
        form = forms.CodeForm(request.POST)

        if form.is_valid():
            code = request.POST['textfield']
            tags = request.POST['tags']
            topic = request.POST['topic']
            list_tags = tags.split(',')
            code_obj = models.Code(code=code, user=request.user, topic=topic)
            code_obj.save()

            for tag in list_tags:
                tag_obj = models.Tag(tag = tag, code=code_obj)
                tag_obj.save()

            return redirect('code:detail', code_id=code_obj.id)
        else:
            return render(request, 'code/create.html', {'form': form})


# Класс Detail
class DetailView(View):
    # метод get, возвращающий страницу просмотра кода
    def get(self, request, code_id):
        code = get_object_or_404(models.Code, id=code_id)
        tags = models.Tag.objects.filter(code = code)
        comments = models.Comment.objects.filter(code = code)
        return render(request, 'code/detail.html', {
            'text': code,
            'tags': tags,
            'comments': comments
            })

# Класс Edit
@method_decorator(login_required, name='dispatch')
class EditView(View):
    # метод get, возвращающий страницу изменения кода
    def get(self, request, code_id):
        code = get_object_or_404(models.Code, id=code_id)
        if request.user == code.user:
            form = forms.CodeForm()
            return render(request, 'code/edit.html', {
                'text': code,
                'form': form
            })
        else:
            add_log_entry(request, request.user, f"GET Попытка изменения кода с id={code.id}")
            return HttpResponseForbidden()

    # метод post, отвечаеющий за обновление данных модели Сode
    def post(self, request, code_id):
        code = get_object_or_404(models.Code, id=code_id)
        tags_obj = models.Tag.objects.filter(code=code_id)

        for obj in tags_obj: # удаление всех тегов, привязанных к коду
            obj.delete()

        if request.user == code.user:
            code.code = request.POST['textfield']
            code.topic = request.POST['topic']
            code.date_last_change = timezone.now()

            try:
                code.save()
            except DataError:
                error = 'Превышен лимит количества символов!'
                add_log_entry(request, request.user, "Превышен лимит количества символов")
                return render(request, 'code/edit.html', {'text': code,'error':error})

            tags = request.POST['tags']
            list_tags = tags.split(',')

            for tag in list_tags: # сохранение новых тегов
                tag_obj = models.Tag(tag = tag, code=code)
                tag_obj.save()

            return redirect('code:detail', code_id=code.id)
        else:
            add_log_entry(request, request.user, f"POST Попытка изменения кода с id={code.id}")
            return HttpResponseForbidden()


# Класс Delete
@method_decorator(login_required, name='dispatch')
class DeleteView(TemplateView):
    template_name = 'code/delete.html'

    # метод get_context_data получает объект code и url, с которого пришел пользователь и возвращает словарь
    def get_context_data(self, code_id):
        code = get_object_or_404(models.Code, id=code_id)
        return_url = self.request.GET.get('next')

        if return_url == None:
            return_url = "/"

        return {'text': code, 'url': return_url} # TODO: return_url сейчас не работает

    # метод post, отвечаеющий за удаление кода
    def post(self, request, code_id):
        code = get_object_or_404(models.Code, id=code_id)

        if request.user == code.user:
            return_url = request.POST['next']

            if return_url == 'None':
                return_url = "/"

            code.delete()
            return HttpResponseRedirect(return_url)
        else:
            add_log_entry(request, request.user, f"POST Попытка удаления кода с id={code.id}")
            return HttpResponseForbidden()


# Класс SearchByTag
@method_decorator(login_required, name='dispatch')
class SearchByTagView(TemplateView):
    template_name = 'code/tagsearch.html'

    # метод get_context_data вовзращает словарь для шаблона tagsearch.html
    def get_context_data(self, tag):
        codes = models.Tag.objects.filter(tag = tag)
        return {'texts': codes, 'tag': tag}

#####################################
# Классы для работы с комментариями #
#####################################
class AllCodeView(View):
    def get(self, request):
        all_codes = models.Code.objects.all()
        paginator = Paginator(all_codes, ENTRIES_COUNT)
        page = request.GET.get('page')
        codes = paginator.get_page(page)
        return render(request, 'code/allcode.html', {'codes': codes})


class CreateCommentView(View):
    def post(self, request, code_id):
        code_obj = get_object_or_404(models.Code, id=code_id)
        form = forms.AddCommentForm(request.POST)

        if form.is_valid():
            comment = request.POST['comment']
            reply_to_id = request.POST['reply_to']
            comm_obj = models.Comment(commentary=comment, user=request.user, code=code_obj)

            if reply_to_id:
                reply_comment = get_object_or_404(models.Comment, id=reply_to_id)
                comm_obj.reply_to = reply_comment

            comm_obj.save()
            return redirect('code:detail', code_id=code_obj.id)
        else:
            code = get_object_or_404(models.Code, id=code_id)
            tags = models.Tag.objects.filter(code = code)
            comments = models.Comment.objects.filter(code = code)
            return render(request, 'code/detail.html', {
                'text': code,
                'tags': tags,
                'comments': comments,
                'form':form
                })

class UpdateCommentView(View):
    def post(self, request, comment_id, code_id):
        comm = get_object_or_404(models.Comment, id=comment_id)
        if request.user == comm.user:
            comm.comment = request.POST['comment']
            comm.save()
            return redirect('code:detail', code_id=code_id)
        else:
            add_log_entry(request, request.user, f"POST Попытка изменения комментария с id={comm.id}")
            return HttpResponseForbidden()

class DeleteCommentView(View):
    def post(self, request, comment_id, code_id):
        comm = get_object_or_404(models.Comment, id=comment_id)
        if request.user == comm.user:
            comm.delete()
            return redirect('code:detail', code_id=code_id)
        else:
            add_log_entry(request, request.user, f"POST Попытка удаления комментария с id={comm.id}")
            return HttpResponseForbidden()
