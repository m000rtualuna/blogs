from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('account/registration/', views.registration, name='registration'),
    path('account/login/', views.MainLoginView.as_view(), name='login'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/profile/', views.profile, name='profile'),
    path('account/profile/edit/', views.EditProfileView.as_view(), name='edit-profile'),
    path('account/profile/delete/', views.DeleteProfileView.as_view(), name='delete-profile'),
    path('create_post/', views.create_post, name='create-post'),
    path('post/<int:pk>/edit_post/', views.edit_post, name='edit-post'),
    path('post/<int:pk>/delete_post/', views.DeletePost.as_view(), name='delete-post'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add-comment'),
    path('post/<int:pk>/toggle_like/', views.toggle_like, name='toggle_like'),
    path('comment/<int:pk>/edit_comment/', views.edit_comment, name='edit-comment'),
    path('comment/<int:pk>/delete_comment/', views.delete_comment, name='delete-comment'),
]