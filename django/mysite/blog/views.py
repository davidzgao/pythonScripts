# -*- coding:utf8 -*-
from django.shortcuts import render,render_to_response
from blog.models import BlogPost,BlogPostForm
from datetime import datetime
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader,Context,RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #添加包

# Create your views here.
def foo(request):
    posts = BlogPost.objects.all()
    #t = loader.get_template("foo.html")
    #c = Context({'posts': posts}) 
    #return HttpResponse(t.render(c))
    return render_to_response('foo.html', {'posts': posts, 'form':BlogPostForm()} ,RequestContext(request))

def create_blogpost(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.timestamp=datetime.now()
            post.save()
#        BlogPost(title = request.POST.get('title'),
#                 body = request.POST.get('body'),
#                 timestamp = datetime.now()                
#                ).save()
    return HttpResponseRedirect('/blog/')

def detail(request,id):
    try:
        post = BlogPost.objects.get(id=str(id))
    except BlogPost.DoseNotExist:
        raise Http404
    return render_to_response("article.html" ,{'post': post } ,RequestContext(request))


def home(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 4) #每页显示两个
    page = request.GET.get('page')
    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.paginator(paginator.num_pages)
    return render_to_response('home.html', {'post_list': post_list } ,RequestContext(request))

def aboutme(request):
    return render_to_response('aboutme.html')

def search_tag_func(request, tag):
    try:
        post_list = BlogPost.objects.filter(category__iexact = tag) #contains
    except BlogPost.DoesNotExist :
        raise Http404
    return render_to_response('tag.html', {'post_list': post_list } ,RequestContext(request))


def search_func(request):
    if 's' in request.GET:
        s = request.GET['s'] 
        print s
        if not s:
            render_to_response('home.html')
        else:
            post_list = BlogPost.objects.filter(title__icontains = s)
            if len(post_list) == 0:
                return render_to_response("home.html" ,{'post_list': post_list, 'not_found': True } ,RequestContext(request))
            else:
                return render_to_response("home.html" ,{'post_list': post_list, 'not_found': False } ,RequestContext(request))


