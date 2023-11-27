from django.urls import path
from .views import *


urlpatterns = [
    path('', index_views, name='index_views'),
    path('register/', register, name='register'),#URLs de Registro y Login
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('about/', about, name='about' ),
    
    # URLs para Item
    path('item/', item_list, name='item_list'),
    path('item/create/', create_item, name='create_item'),
    path('item/<int:item_id>/update/', update_item, name='update_item'),
    path('item/<int:item_id>/delete/', delete_item, name='delete_item'),
    path('item/main/', item_main, name = 'item_main'),
    
    # URLs para Posts
    path('posts/', post_list, name='post_list'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:post_id>/update/', update_post, name='update_post'),
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('post/main/', post_main, name = 'post_main'),


    # Puedes agregar más URLs según sea necesario
]
