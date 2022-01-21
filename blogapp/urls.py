from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.MainView, name='MainView'),
    path('post/<int:pk>', views.PostDetailView, name='PostDetailView'),
    path('post/create', views.PostCreateView.as_view(), name='PostCreateView'),
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='PostEditView'),

] 