from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('',views.index,name='index'),
    path('posts/',views.PostListView.as_view(),name='post'),
    path('posts/<int:id>',views.post_detail,name='post_detail'),
    path('posts/<int:id>/comments/', views.post_comment, name='comments'),
    path('posts/add',views.postForm,name='post_add'),
    # path('posts/<pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('tickets/',views.ticket,name='ticket'),
    path('search/',views.post_search,name='post_search'),

]