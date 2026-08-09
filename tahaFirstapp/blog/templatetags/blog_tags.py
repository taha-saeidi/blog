from idlelib import replace
from unicodedata import name
import re
from django.db.models import Count, Max, Min, Q
from django import template

from . import bad_words
from .bad_words import BAD_WORDS
from ..models import Post, Comment
from django.contrib.auth.models import User
# from django.db.models import Max

register = template.Library()


@register.simple_tag(name="tp")
def total_post():
    return Post.Published_Manager.count()


@register.simple_tag(name="tc")
def total_comments():
    return Comment.objects.count()


@register.simple_tag(name="lp")
def last_post():
    return Post.Published_Manager.first().published
@register.inclusion_tag("partials/most_comment.html" ,name="cm")
def most_popular_posts(count=5):
    post_comments = Post.Published_Manager.annotate(comment_count=Count("comment")).order_by('-comment_count')[:count]

    context = {
        'post_comments': post_comments,
    }
    return context
# @register.simple_tag(name="top")
# def top_post_comments():
#     for post in Post.Published_Manager.all():
#         i = post
#         if post.comment.count()>
@register.inclusion_tag("partials/latest_posts.html" ,name="lpt")
def latest_posts(count=5):
    l_post = Post.Published_Manager.order_by('-published')[:count]
    context = {
        'l_post': l_post,
    }
    return context
#
@register.inclusion_tag("partials/count_post.html" ,name="cp")
def count_latest_posts(count=5):
    count_post = Post.Published_Manager.order_by('-published')[:count].count()
    context = {
        'count_post': count_post,
    }
    return context

@register.inclusion_tag("partials/authors.html" ,name="aut")
def authors():
    users = User.objects.all()
    id = User.objects.all().values_list('id', flat=True)
    context = {
        'users': users,
        'id': id,
    }
    return context
@register.inclusion_tag("partials/most_reading_time_post.html",name="mr")
def most_reading_time_posts():
    # most_reading_time = Post.Published_Manager.aggregate(Max('reading_time')).get("reading_time__max")
    most_reading_time = Post.Published_Manager.annotate(reading_time_count=Max("reading_time")).order_by('-reading_time_count')[0]
    time = Post.Published_Manager.get(id=most_reading_time.id).reading_time

    context = {
        'mrt': most_reading_time,
        'time': time,
    }
    return context

@register.inclusion_tag("partials/most_min_reading_time_post.html",name="min-mr")
def min_most_reading_time_posts():
    min_most_reading_time = Post.Published_Manager.annotate(min_reading_time_count=Min("reading_time")).order_by('min_reading_time_count')[0]
    time= Post.Published_Manager.get(id=min_most_reading_time.id).reading_time

    context = {
        'min': min_most_reading_time,
        'time': time,
    }
    return context

#bad words :
BAD_WORDS = bad_words.BAD_WORDS
#cesor description text
@register.filter(name = "censor", is_safe=True)
def censor_text(value):
    if value:
        for word in BAD_WORDS:
            #جایگزینی با ستاره به اندازه تعداد کلمات
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            replacement = "*"*len(word)
            value = re.sub(pattern,replacement, value)
        return value
    else:
        return value


# @register.inclusion_tag("partials/active_author.html" ,name="active-author")
@register.inclusion_tag("partials/active_author.html", name="active-author")
def active_author():

    author = User.objects.annotate(
        post_count=Count(
            "user_post",
            filter=Q(user_post__status=Post.Status.PUBLISHED)
        )
    ).order_by("-post_count").first()

    context = {
        'author': author,
    }
    return context

@register.inclusion_tag("partials/in_active_author.html", name="in_active-author")
def inactive_author():
    author = User.objects.annotate(
        post_count=Count(
            "user_post",
            filter=Q(user_post__status=Post.Status.PUBLISHED)
        )
    ).filter(
        post_count__gt=0
    ).order_by("post_count").first()

    return {
        "author": author,
    }

















