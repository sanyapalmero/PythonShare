from django.urls import include, path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:text_id>', views.detail, name='detail'),
]
