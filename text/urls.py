from django.urls import include, path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('codeid/<int:text_id>', views.DetailView.as_view(), name='detail'),
    path('edit/<int:text_id>', views.EditView.as_view(), name='edit'),
    path('delete/<int:text_id>', views.DeleteView.as_view(), name='delete'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('search/<str:tag>', views.SearchByTagView.as_view(), name='search'),
    path('all/', views.AllCodeView.as_view(), name='all'),
    path(
        'addcomment/<int:text_id>',
        views.CreateCommentView.as_view(),
        name='addcomment'),
    path(
        'updcomment/<int:comment_id>/<int:text_id>',
        views.UpdateCommentView.as_view(),
        name='updcomment'),
    path(
        'delcomment/<int:comment_id>/<int:text_id>',
        views.DeleteCommentView.as_view(),
        name='delcomment')
]
