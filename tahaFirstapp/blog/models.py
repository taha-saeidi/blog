#moduls
from django.utils import timezone

from datetime import timezone

from django.db import models
from django.utils import timezone, module_loading
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
#manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "PB" , "Published"
        DRAFT = "DF" , "Draft"
        Rejected = "R" , "Rejected"
    #relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post" , verbose_name = "نویسنده")
    #data fields
    title = models.CharField(max_length=250, verbose_name = "عنوان")
    description = models.TextField(verbose_name = "توضیحات")
    slug = models.SlugField(max_length=250)
    #date
    published = models.jDateTimeField(default=timezone.now)
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "زمان تولید")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name = "زمان آپدیت")
    #choices fields
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT
                              , verbose_name=" وضعیت پست"
                              )
    reading_time = models.PositiveIntegerField(default=0 , verbose_name="زمان مطالعه")

    # objects = models.Manager()
    objects = jmodels.Manager()
    Published_Manager = PublishedManager()
    def get_absolute_url(self):
        return reverse("blog:post_detail", args={self.id})
    class Meta:
        ordering = ('-published',)
        indexes = [
        models.Index(fields=['-published']),
        ]
        verbose_name = "پست ها"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class Ticket(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=250)

    class Meta:
        verbose_name = "تیکت ها"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment" , verbose_name="پست")
    body = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name="اسم")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان تولید")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان آپدیت")
    # published = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=False,verbose_name="وضعیت")

    class Meta:
        ordering = ('created',)
        indexes = [
        models.Index(fields=['created']),
        ]
        verbose_name = " کامنت ها "
        verbose_name_plural = verbose_name
    def __str__(self):
        return f"{self.name}:{self.post}"



































