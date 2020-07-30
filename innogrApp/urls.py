from django.contrib.auth import admin
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    UserProfileListView,
    postpreference,
    
)

from . import views

# rests api routes
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('index.html', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('profile/<str:user>', UserProfileListView.as_view(), name='profile-posts'),
    # url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$', postpreference, name='postpreference'),
    path('posts/<int:postid>/preference/<int:userpreference>', views.postpreference, name='postpreference'),
    
    # restapi url
    path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    path('myDevices', views.mydevices, name='MyDevices'),
    path('newsFeed', views.newsFeed, name='MynewsFeed'),
    # path('Profile/Overview', views.profilepage, name='profilepage'),
    path('Profile/Settings', views.Accountsettings, name='Accountsettings'),
    path('Resources/Support', views.Resources, name='Resources'),

]