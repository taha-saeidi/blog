from urllib import parse

from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

# Register your models here.
admin.sites.AdminSite.site_title = "پنل ادمین"
admin.sites.AdminSite.site_header = "پنل مدیریت"
admin.sites.AdminSite.index_title = "دسته بندی ها"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'status',"reading_time",)
    ordering = ('-published',)
    list_filter = ('status', ('published',JDateFieldListFilter), 'author', )
    search_fields = ('title', 'description')
    raw_id_fields = ('author',)
    date_hierarchy = 'published'
    prepopulated_fields = {'slug': ["title"]}
    list_editable = ('status', )
    # list_display_links = ('author',)
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name',  'phone','subject',)
    list_filter = ('subject',)
    # list_editable = ('subject',)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','name','created' , 'active',)
    list_filter = ('active',('created',JDateFieldListFilter),('updated',JDateFieldListFilter),)
    ordering = ('-created',)
    search_fields = ('name','body',)
    list_editable = ('active',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('post','title','created')