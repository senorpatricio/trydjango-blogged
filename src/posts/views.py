from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Successfully created!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created!")    
    # if request.method == "POST":
    #     print request.POST.get('content')
    #     print request.POST.get('title')
    context = {
        'form': form,
    }
    return render(request, 'post_form.html', context)

def post_detail(request, id=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset_list = Post.objects.all().order_by("-timestamp") # this will order it by newes
    paginator = Paginator(queryset_list, 5) # Show 5 objects per page
    # page_request_var = "abc"
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        # "page_request_var": page_request_var
    }

    # if request.user.is_authenticated():  //this checks to see if the user is authenticated
    #     context = {
    #         "title": "My User List"
    #     }
    # else:
    #     context = {
    #         "title": "List"
    #     }

    return render(request, "post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():  #allows you to edit using the same create form
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Successfully updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted!")
    return redirect("posts:list")
