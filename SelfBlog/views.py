from django.shortcuts import render,redirect
from SelfBlog.models import *
from django.views.decorators.csrf import csrf_exempt

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
    # message=Message()
    # wo=''
    # if request.method=='POST':
    #
    #     mes=request.POST.get('message')
    #     if mes:
    #         message.message=mes
    #         message.article=article
    #         message.save()
    #         wo='提交成功！'
    #     # print(mes)
    #     else:
    #         wo='请输入评论内容！'

    mess=Message.objects.filter(article_id=article_id).order_by('-times')[:3]
    message_counts=Message.objects.filter(article_id=article_id).count()
    article.comment_count=message_counts
    article.read_count=read_count+1
    article.save()

    return render(request,'detail.html',{'article':article,'mess':mess,'message_counts':message_counts})
@csrf_exempt
def messages(request):
    if request.is_ajax():
        message=Message()
        data = request.POST
        print(data)
        mes=request.POST.get('comm')
        article_id=request.POST.get('article_id')
        articles=Article.objects.get(id=article_id)
        if mes:
            message.message = mes
            message.article = articles
            message.save()
        return redirect('/detail/&article_id='+article_id+'/')


def typearticle(request,types):
    type_id=Types.objects.filter(types=types).values()[0]['id']
    print(type_id)
    typearts=Article.objects.filter(types=type_id)
    return render(request,'typearticle.html',{'typearts':typearts})

def self_center(request):
    return render(request,'self_center.html')