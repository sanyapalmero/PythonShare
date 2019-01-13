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

from .forms import AddCommentForm, CodeForm
from .models import Code, Tag, Comment

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
        template_name = 'code/index.html'
        return render(request, template_name)


# Класс Сreate
@method_decorator(login_required, name='dispatch')
class CreateView(View):
    # метод get, возвращающий страницу create.html
    def get(self, request):
        template_name = 'code/create.html'
        form = CodeForm()
        return render(request, template_name, {'form': form})

    # метод post, отвечающий за добавление кода
    def post(self, request):
        template_name = 'code/create.html'
        form = CodeForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['codefield']
            tags = form.cleaned_data['tags']
            topic = form.cleaned_data['topic']
            list_tags = tags.split(',')
            code_model = Code(code=code, user=request.user, topic=topic)
            code_model.save()

            for tag in list_tags:
                tag_model = Tag(tag = tag, code=code_model)
                tag_model.save()

            return redirect('code:detail', code_id=code_model.id)
        else:
            return render(request, template_name, {'form': form})


# Класс Detail
class DetailView(View):
    # метод get, возвращающий страницу просмотра кода
    def get(self, request, code_id):
        template_name = 'code/detail.html'
        code = get_object_or_404(Code, id=code_id)
        tags = Tag.objects.filter(code = code)
        comments = Comment.objects.filter(code = code)

        return_url = self.request.GET.get('next')
        if return_url == None:
            return_url = "/"

        return render(request, template_name, {
            'code': code,
            'tags': tags,
            'comments': comments,
            'url': return_url
            })

# Класс Edit
@method_decorator(login_required, name='dispatch')
class EditView(View):
    # метод get, возвращающий страницу изменения кода
    def get(self, request, code_id):
        template_name = 'code/edit.html'
        code = get_object_or_404(Code, id=code_id)
        if request.user == code.user:
            form = CodeForm()
            return render(request, template_name, {
                'code': code,
                'form': form
            })
        else:
            add_log_entry(request, request.user, f"GET Попытка изменения кода с id={code.id}")
            return HttpResponseForbidden()

    # метод post, отвечаеющий за обновление данных модели Сode
    def post(self, request, code_id):
        template_name = 'code/edit.html'
        code = get_object_or_404(Code, id=code_id)
        tags = Tag.objects.filter(code=code_id)

        for tag in tags: # удаление всех тегов, привязанных к коду
            tag.delete()

        if request.user == code.user:
            code.code = request.POST['codefield']
            code.topic = request.POST['topic']
            code.date_last_change = timezone.now()
            code.save()

            new_tags = request.POST['tags']
            list_tags = new_tags.split(',')

            for tag in list_tags: # сохранение новых тегов
                tag_model = Tag(tag=tag, code=code)
                tag_model.save()

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
        code = get_object_or_404(Code, id=code_id)
        return_url = self.request.GET.get('next')

        if return_url == None:
            return_url = "/"

        return {'code': code, 'url': return_url}

    # метод post, отвечаеющий за удаление кода
    def post(self, request, code_id):
        code = get_object_or_404(Code, id=code_id)

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
        codes = Tag.objects.filter(tag = tag)
        return {'codes': codes, 'tag': tag}

#####################################
# Классы для работы с комментариями #
#####################################
class AllCodeView(View):
    def get(self, request):
        template_name = 'code/allcode.html'
        all_code_models = Code.objects.all()
        paginator = Paginator(all_code_models, ENTRIES_COUNT)
        page = request.GET.get('page')
        codes = paginator.get_page(page)
        return render(request, template_name, {'codes': codes})


class CreateCommentView(View):
    def post(self, request, code_id):
        template_name = 'code/detail.html'
        code_model = get_object_or_404(Code, id=code_id)
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data['comment']
            reply_to_id = form.changed_data['reply_to']
            comment_model = Comment(commentary=comment, user=request.user, code=code_model)

            if reply_to_id:
                reply_comment = get_object_or_404(Comment, id=reply_to_id)
                comment_model.reply_to = reply_comment

            comment_model.save()
            return redirect('code:detail', code_id=code_model.id)
        else:
            code = get_object_or_404(Code, id=code_id)
            tags = Tag.objects.filter(code = code)
            comments = Comment.objects.filter(code = code)
            return render(request, template_name, {
                'code': code,
                'tags': tags,
                'comments': comments,
                'form':form
                })

class UpdateCommentView(View):
    def post(self, request, comment_id, code_id):
        comment_model = get_object_or_404(Comment, id=comment_id)
        if request.user == comm.user:
            comment_model.comment = request.POST['comment']
            comment_model.save()
            return redirect('code:detail', code_id=code_id)
        else:
            add_log_entry(request, request.user, f"POST Попытка изменения комментария с id={comment_model.id}")
            return HttpResponseForbidden()

class DeleteCommentView(View):
    def post(self, request, comment_id, code_id):
        comment_model = get_object_or_404(Comment, id=comment_id)
        if request.user == comm.user:
            comment_model.delete()
            return redirect('code:detail', code_id=code_id)
        else:
            add_log_entry(request, request.user, f"POST Попытка удаления комментария с id={comment_model.id}")
            return HttpResponseForbidden()
