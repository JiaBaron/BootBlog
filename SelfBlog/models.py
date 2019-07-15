from django.db import models
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=64,null=False,verbose_name='标题')
    content=RichTextField(verbose_name='正文')
    images=models.ImageField(upload_to='images')
    read_count=models.IntegerField(default=0,verbose_name='阅读数')
    comment_count=models.IntegerField(default=0,verbose_name='评论数')
    times=models.DateTimeField(auto_now_add=True)
    types=models.ForeignKey('Types')
    def __str__(self):
        return self.title

class Types(models.Model):
    types=models.CharField(max_length=32)
    def __str__(self):
        return self.types

class Message(models.Model):
    message=RichTextField(verbose_name='评论')
    article=models.ForeignKey('Article')
    times=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    def __str__(self):
        return self.message
