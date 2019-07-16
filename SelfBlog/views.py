from django.shortcuts import render
from SelfBlog.models import *

# Create your views here.

def base(request):
    article_list=Article.objects.all()
    article_count=article_list.count()           #文章数量
    message_count=Message.objects.count()        #评论数量
    type_list={}                                 #用于存放每种类型及其对应的文章数量
    types=Types.objects.all()
    for ts in types:
        ts_count=Article.objects.filter(types=ts).count()
        type_list[ts]=ts_count
    # print(type_list)
    popular_article={}

    most_read_article_list=article_list.order_by('-read_count')[:2]
    print(most_read_article_list)     #<QuerySet [<Article: 浅拷贝与深拷贝>, <Article: Python while循环乘法口诀，for循环乘法口诀>]>
    for art in most_read_article_list:
        art_xq = {}
        re_coun=article_list.get(title=art).read_count        #该文章阅读量

        art_id=article_list.get(title=art).id
        art_xq[str(re_coun)]=art_id
        popular_article[art]=art_xq

    return render(request,'base.html',{'article_list':article_list,'article_count':article_count,'message_count':message_count
                                       ,'type_list':type_list,'popular_article':popular_article})

def detail(request,id):
    article_id=int(id)
    article=Article.objects.get(id=article_id)
    read_count=article.read_count
    message=Message()
    if request.method=='POST':
        mes=request.POST.get('message')
        message.message=mes
        message.article=article
        message.save()
        # print(mes)
    mess=Message.objects.filter(article_id=article_id)
    message_counts=Message.objects.filter(article_id=article_id).count()
    article.comment_count=message_counts
    article.read_count=read_count+1
    article.save()

    return render(request,'detail.html',{'article':article,'mess':mess,'message_counts':message_counts})