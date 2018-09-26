from django.urls import include, path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddView.as_view(), name='add'),
    path('upd/<int:text_id>', views.UpdView.as_view(), name='upd'),
    path('text/<int:text_id>', views.DetailView.as_view(), name='detail'),
    path('edit/<int:text_id>', views.EditView.as_view(), name='edit'),
]
