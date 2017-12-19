# from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post #
from .forms import EmailPostForm
from django.core.mail import send_mail
import os

# def post_list(request):
  # # posts = Post.published.all()
  # object_list = Post.published.all()
  # paginator = Paginator(object_list, 3) # 3 posts in each page
  # page = request.GET.get('page')
  # try:
    # posts = paginator.page(page)
  # except PageNotAnInteger:
    # # If page is not an int, deliver the first page
    # posts = paginator.page(1)
  # except EmptyPage:
    # # if page is out of range, deliver last page of results
    # posts = paginator.page(paginator.num_pages)
 
  # return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

# TODO try using model=Post instead


class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts' # object_list
  paginate_by = 3
  template_name = 'blog/post/list.html' # blog/post_list.html


def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
  return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
  post = get_object_or_404(Post, id=post_id, status='published')
  sent = False

  if request.method=='POST':
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = '{} ({}) recommends you reading "{}"'\
        .format(cd['name'], cd['email'], post.title)
      message = 'Read "{}" at {}\n\n{}\'s comments: {}'\
        .format(post.title, post_url, cd['name'], cd['comments'])
      send_mail(subject, message, os.environ['EMAILUSER'], [cd['to']])
      sent = True
  else:
    form = EmailPostForm()
  return render(request, 'blog/post/share.html', {'post': post,
                                                  'form': form,
                                                  'sent': sent})

