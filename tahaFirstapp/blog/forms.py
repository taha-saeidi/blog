from tokenize import Comment

from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # STATUS_CHOICES = (
        #     ('Published', 'Published'),
        #     ('Rejected', 'Rejected'),
        #     ('Draft', 'Draft'),
        # )
        # status = forms.ChoiceField(choices=STATUS_CHOICES)
        fields = ('author','title', 'description', 'slug','reading_time',)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            if len(title) < 3:
                raise forms.ValidationError("نام وارد شده کوتاه است !")
            elif len(title) > 25:
                raise forms.ValidationError("نام وارد شده بلند است !")
            else:
                return title
        return None
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug:
            if len(slug) < 3:
                raise forms.ValidationError("اسلاگ وارد شده کوتاه است !")
            elif len(slug) > 25:
                raise forms.ValidationError("اسلاگ وارد شده بلند است !")
            else:
                return slug
        return None
    # def clean_reading_time(self):
    #     reading_time = self.cleaned_data['reading_time']
    #     if reading_time:
    #         if not reading_time.isnumeric():
    #             raise forms.ValidationError("زمان مطالعه باید به صورت عدد مثبت وارد شود!")
    #         # elif reading_time<0 or reading_time==0:
    #         #     raise forms.ValidationError("زمان مطالعه نباید عدد منفی باشد !")
    #         else:
    #             return reading_time
    #     return None



#ticket form
class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
    ('گزارش', 'گزارش'),
    ('انتقاد', 'انتقاد'),
    ('پیشنهاد', 'پیشنهاد'),
    )
    message = forms.CharField(widget=forms.Textarea , required=True)
    name = forms.CharField(max_length=250 , required=True)
    email = forms.CharField(max_length=250)
    phone = forms.CharField(max_length=11 , required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError ("شماره شما به صورت عددی وارد نشده است ")
            elif len(phone) != 11:
                raise forms.ValidationError("مقدار وارد شده برای شماره تلفن صحیح نمیباشد (11) کاراکتر!!")
            else:
                return phone
        return None
class CommentForm(forms.ModelForm):
    def clean_name(self):
            name = self.cleaned_data['name']
            if name:
                if len(name) <3 :
                    raise forms.ValidationError("نام وارد شده کوتاه است !")
                else:
                    return name
            return None
    class Meta:

        model = Comment
        fields = ('name', 'body',)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=250 , required=True)
