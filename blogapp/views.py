
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from .models import Post, Category

from django.shortcuts import render, get_object_or_404

def MainView(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    category = ''
    if request.method == 'GET':
        if 'category' in request.GET:
            category = request.GET['category']
            if category != 'All':
                posts = Post.objects.filter(category__name=category)
    ctx = {'posts' : posts.order_by('-post_date'), 'category' : category, 'categories' : categories}
    return render(request, 'blogapp/mainview.html', ctx)

def PostDetailView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogapp/postview.html', {'post': post})

'''
def LikePost(request, pk):
    post = Post.objects.get(pk=pk)
    post.likes = post.likes + 1
    post.save()
    messages.info(request, 'I\'m glad you liked the article. Thank you for reading!')
    return redirect('blog:PostDetailView', pk)
'''
#@method_decorator(login_required(), 'dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title','author', 'body', 'snippet', 'category']
    success_url = reverse_lazy('blog:MainView')
    def form_valid(self, form):
        object = form.save(commit=False)
       
        object.save()
        post = Post.objects.get(pk=object.pk)
        messages.info(self.request, 'Your post is saved and sent for review. Once it is approved, it will be published.')
        return super(PostCreateView, self).form_valid(form)

#@method_decorator(login_required(), 'dispatch')
class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'body', 'snippet', 'category']
    success_url = reverse_lazy('blog:MainView')
    def get_queryset(self):
        qs = super(PostEditView, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=self.request.user, locked=False)

'''@login_required()
def MyArticlesView(request):
    posts = Post.objects.filter(author=request.user)
    categories = []
    for post in posts:
        if not post.category in categories:
            categories.append(post.category)
    category = ''
    if request.method == 'GET':
        if 'category' in request.GET:
            category = request.GET['category']
            if category != 'All':
                posts = posts.filter(category__name=category)
    ctx = {'posts' : posts.order_by('-post_date'), 'category' : category, 'categories' : categories, 
        'view' : 'MyArticlesView'}
    return render(request, 'blogapp/mainview.html', ctx)
'''
'''
@login_required()
@user_passes_test(lambda u:u.is_superuser, login_url='blog:NoAccess')
def ApprovePost(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.visible = True
        post.locked = True
        post.save()
        messages.info(request, 'Post is approved and visible in Ozan.pl blog page.')
        return redirect('blog:MainView')
    return render(request, 'blogapp/postapprove.html', {'post' : post})

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            messages.success(request, 'You logged in successfully...')
            return redirect('blog:MainView')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    ctx = {}
    return render(request, 'login.html', ctx)

def LogoutView(request):
    messages.info(request, 'Successfully logged out...')
    logout(request)
    return redirect('blog:LoginView')
    '''