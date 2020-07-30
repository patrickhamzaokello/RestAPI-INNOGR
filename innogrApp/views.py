from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Preference
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import sys
from django.db.models import Count, Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm

# rest api view
from rest_framework import viewsets
from .serializers import Postserializer
# from .models import Post

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('title')
    serializer_class = Postserializer


# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'innogrApp/index.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-likes']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.exclude(author=self.request.user).values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-author_count')\
            .first()
            # .aggregate(Max('author_count'))
            
        print(data_counter)
        usergot = User.objects.filter(pk=data_counter['author']).first()
        all_users.append(usergot)
        # if Preference.objects.get(user = self.request.user):
        #     data['preference'] = True
        # else:
        #     data['preference'] = False
        data['preference'] = Preference.objects.all()
        # print(Preference.objects.get(user= self.request.user))
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'innogrApp/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.exclude(author=self.request.user).values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-author_count')[0:6]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author']).first())
        # if Preference.objects.get(user = self.request.user):
        #     data['preference'] = True
        # else:
        #     data['preference'] = False
        data['preference'] = Preference.objects.all()
        # print(Preference.objects.get(user= self.request.user))
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class UserProfileListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'innogrApp/profile_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.exclude(author=self.request.user).values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-author_count')

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author']).first())
        # if Preference.objects.get(user = self.request.user):
        #     data['preference'] = True
        # else:
        #     data['preference'] = False
        data['preference'] = Preference.objects.all()
        # print(Preference.objects.get(user= self.request.user))
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('user'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','summary', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','summary', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
@login_required
def postpreference(request, postid, userpreference):

    
        
        if request.method == "POST":
                eachpost= get_object_or_404(Post, id=postid)

                obj=''

                valueobj=''

                try:
                        obj= Preference.objects.get(user= request.user, post= eachpost)

                        valueobj= obj.value #value of userpreference


                        valueobj= int(valueobj)

                        userpreference= int(userpreference)
                
                        if valueobj != userpreference:
                                obj.delete()


                                upref= Preference()
                                upref.user= request.user

                                upref.post= eachpost

                                upref.value= userpreference


                                if userpreference == 1 and valueobj != 1:
                                        eachpost.likes += 1
                                        eachpost.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        eachpost.dislikes += 1
                                        eachpost.likes -= 1
                                

                                upref.save()

                                eachpost.save()
                        
                        
                                context= {'eachpost': eachpost,
                                  'postid': postid}

                                return redirect('post-detail',pk=postid)

                        elif valueobj == userpreference:
                                obj.delete()
                        
                                if userpreference == 1:
                                        eachpost.likes -= 1
                                elif userpreference == 2:
                                        eachpost.dislikes -= 1

                                eachpost.save()

                                context= {'eachpost': eachpost,
                                  'postid': postid}

                                return redirect('post-detail',pk=postid)
                                
                        
        
                
                except Preference.DoesNotExist:
                        upref= Preference()

                        upref.user= request.user

                        upref.post= eachpost

                        upref.value= userpreference

                        userpreference= int(userpreference)

                        if userpreference == 1:
                                eachpost.likes += 1
                        elif userpreference == 2:
                                eachpost.dislikes +=1

                        upref.save()

                        eachpost.save()                            


                        context= {'eachpost': eachpost,
                          'postid': postid}

                        return redirect('post-detail',pk=postid)


        else:
                eachpost= get_object_or_404(Post, id=postid)
                context= {'eachpost': eachpost,
                          'postid': postid}

                return redirect('post-detail',pk=postid)
            
            
            

@login_required
def mydevices(request):
    return render(request,'innogrApp/pages/mydevices.html')

@login_required
def newsFeed(request):
    context = {
        'posts': Post.objects.all().order_by('-date_posted'),
    }
    return render(request,'innogrApp/pages/newsfeed.html', context)

# @login_required
# def profilepage(request):
#     mypost = {
#         'posts': Post.objects.all().order_by('-date_posted')
#     }
#     return render(request, 'innogrApp/pages/profile/overview.html',mypost)

@login_required
def Accountsettings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('profile-posts', user= request.user.username)
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form': p_form
    }

    return render(request, 'innogrApp/pages/profile/settings.html', context)

@login_required
def Resources(request):
    return render(request, 'innogrApp/pages/government/supportcenters.html')

