from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count  

from .models import Post
from .utils import *
from .forms import PostForm
# from users.models import Follow, CustomUser

def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    posts = Post.objects.all()

    paginator = Paginator(posts, 3)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    
    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url, 
        'prev_url': prev_url
    }

    return render(request, 'blog/index.html', context=context)

# def is_users(post_user, logged_user):
#     return post_user == logged_user

#     return render(request, 'blog/index.html')


PAGINATION_COUNT = 3



# class PostListView(LoginRequiredMixin, ListView):
#     model = Post
#     template = 'blog/index.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = PAGINATION_COUNT

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)

#         all_users = []
#         data_counter = Post.objects.values('author')\
#             .annotate(author_count=Count('author'))\
#             .order_by('-author_count')[:6]

#         for aux in data_counter:
#             all_users.append(User.objects.filter(pk=aux['author']).first())
        
#         data['all_users'] = all_users
#         print(all_users, file=sys.stderr)
#         return data

#     # def get_queryset(self):
#     #     user = self.request.user
#     #     qs = Follow.objects.filter(user=user)
#     #     follows = [user]
#     #     for obj in qs:
#     #         follows.append(obj.follow_user)
#     #     return Post.objects.filter(author__in=follows).order_by('-date_posted')


# class PostDetail(ObjectDetailMixin, View):
#     model = Post
#     template = 'blog/post_detail.html'
#     context_object_name = 'post'

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
#         data['comments'] = comments_connected
#         data['form'] = NewCommentForm(instance=self.request.user)
#         return data

#     def post(self, request, *args, **kwargs):
#         new_comment = Comment(content=request.POST.get('content'),
#                               author=self.request.user,
#                               post_connected=self.get_object())
#         new_comment.save()

#         return self.get(self, request, *args, **kwargs)


# class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
#     model_form = PostForm
#     template = 'blog/post_create_form.html'
#     raise_exception = True
#     fields = ['content']
#     success_url = '/'


#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['tag_line'] = 'Add a new post'
#         return data

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    fields = ['content']
    template = 'blog/post_update_form.html'
    raise_exception = True
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Edit a post'
        return data


# class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
#     model =Post
#     template = 'blog/post_delete_form.html'
#     redirect_url = 'posts_list_url'
#     raise_exception = True

#     def test_func(self):
#         return is_users(self.get_object().author, self.request.user)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT


    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)




# class FollowsListView(ListView):
#     model = Follow
#     template_name = 'blog/follow.html'
#     context_object_name = 'follows'

#     def visible_user(self):
#         return get_object_or_404(User, username=self.kwargs.get('username'))

#     def get_queryset(self):
#         user = self.visible_user()
#         return Follow.objects.filter(user=user).order_by('-date')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['follow'] = 'follows'
#         return data


# class FollowersListView(ListView):
#     model = Follow
#     template_name = 'blog/follow.html'
#     context_object_name = 'follows'

#     def visible_user(self):
#         return get_object_or_404(User, username=self.kwargs.get('username'))

#     def get_queryset(self):
#         user = self.visible_user()
#         return Follow.objects.filter(follow_user=user).order_by('-date')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['follow'] = 'followers'
#         return data

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'
    


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


# class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
#     model = Post
#     model_form = PostForm
#     template = 'blog/post_update_form.html'
#     raise_exception = True



class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model =Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True

