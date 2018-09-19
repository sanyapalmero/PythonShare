from django.urls import include, path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('upd/<int:text_id>', views.upd, name='upd'),
    path('text/<int:text_id>', views.detail, name='detail'),
    path('edit/<int:text_id>', views.edit, name='edit'),
]
