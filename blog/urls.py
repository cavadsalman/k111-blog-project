from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog-list'),
    path('article/<int:id>/', views.blog_detail, name='blog-detail'),
    path('add-article/', views.add_article, name='add-article'),
    path('confirm-add-article/', views.confirm_add_article, name='confirm-add-article'),
    path('edit-article/<int:pk>/', views.edit_article, name='edit-article'),
    path('confirm-edit-article/<int:pk>/', views.confirm_edit_article, name='confirm-edit-article'),
    path('confirm-delete-article/<int:pk>/', views.confirm_delete_article, name='confirm-delete-article'),
    path('review/<int:pk>/<int:star_count>/', views.review, name='review'),
]
