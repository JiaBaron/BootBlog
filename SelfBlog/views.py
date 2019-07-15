from django.shortcuts import render
from SelfBlog.models import *

# Create your views here.

def base(request):
    article_list=Article.objects.all()
    return render(request,'base.html',{'article_list':article_list})

def detail(request):
    return render(request,'detail.html')