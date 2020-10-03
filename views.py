from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from .models import Post
from django.views.generic import (
                                ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView
)

# posts = [
#     {
#         'author': 'Nitin',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 4, 2018'
#     },
#     {
#         'author': 'Rahul yadav',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 5, 2018'
#     }
# ]

def home(request):
    context={
        'posts':Post.objects.all()
        }
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html')

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=2

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html')
