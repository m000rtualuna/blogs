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
    path('account/profile/delete/', views.profile, name='delete-profile'),
    path('create_post/', views.create_post, name='create_post'),
]