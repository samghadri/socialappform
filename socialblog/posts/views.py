from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.htttp import Http404
from braces.views import SelectRelatedMixins
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model


class PostList(SelectRelatedMixins,generic.ListView):
    model = Post
    select_related = ('user','group')


class UserPost(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post.user = User.objects.prefetch_related('posts').get(username__iexact=self.page_kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixins,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin,SelectRelatedMixins,generic.CreateView):
    fields = ('message','group')
    model = models.Post

    def form_valid(self):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixins,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')


    def get_queryset(self):
        queryset = super().get_queryset
        return queryset.filter(user_id=self.request.user.id)


    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Successfully Deleted!')
        return super().delete(*args,**kwargs)
