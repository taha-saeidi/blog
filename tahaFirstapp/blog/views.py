import email
from pydoc import describe

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from .models import *
from .forms import *
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, ListView
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    # return HttpResponse("index page")
    return render(request, 'blog/index.html')


# def post(request):
    posts = Post.Published_Manager.all()
#     paginator = Paginator(posts,2)
#     page_number = request.GET.get('page',1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context = {'posts':posts}
#     return render(request,'blog/list.html',context)
class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'
    queryset = Post.Published_Manager.all()


def post_detail(request,id):
    post = get_object_or_404(Post, id=id , status=Post.Status.PUBLISHED)
    comments = post.comment.filter(active = True)
    form = CommentForm()
    context = {'post':post,
               'form':form, 
               'comments':comments,
               }
    return render(request,'blog/detail.html',context)
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create(name=cd['name'], email=cd['email'],
                                               message=cd['message'], phone=cd['phone'],
                                               subject=cd['subject'])
            # ticket_obj.message = cd['message']
            # ticket_obj.name = cd['name']
            # ticket_obj.email = cd['email']
            # ticket_obj.subject = cd['subject']
            #ticket_obj.phone = cd['phone']
            # ticket_obj.save()
            return redirect('blog:index')
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request,id):
    post = get_object_or_404(Post, id=id , status=Post.Status.PUBLISHED)
    comment= None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {'post':post,'form':form,'comment':comment}
    return render(request,'forms/comment.html',context)



def postForm(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Post.objects.create(author=cd['author'],title=cd['title'], description=cd['description'],
                                               slug=cd['slug'],reading_time = cd['reading_time'],
                                               )
            # ticket_obj.message = cd['message']
            # ticket_obj.name = cd['name']
            # ticket_obj.email = cd['email']
            # ticket_obj.subject = cd['subject']
            # ticket_obj.phone = cd['phone']
            # ticket_obj.save()
            return redirect('blog:index')
    else:
        form = PostForm()

    return render(request, 'forms/postForm.html', {'form': form})

def post_search(request):
    query = None
    resault = []
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # resault_1 =Post.Published_Manager.filter(title__icontains=query)
            # resault_2 = Post.Published_Manager.filter(description__icontains=query)
            # resault = resault_1 | resault_2
    context = {'resault':resault,'query':query}
    return render(request, 'blog/search.html',context)


















