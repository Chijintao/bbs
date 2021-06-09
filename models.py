from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


# 用户表
class Userinfo(AbstractUser):
    phone = models.CharField(verbose_name='手机号', max_length=32, null=True, blank=True)
    avatar = models.FileField(verbose_name='头像', upload_to='avatar/', default='avatar/default.jpg')
    create_time = models.DateField(verbose_name='注册时间', auto_now_add=True)
    blog = models.OneToOneField(to='Blog', null=True)

    def __str__(self):
        return self.username


# 站点表
class Blog(models.Model):
    site_name = models.CharField(verbose_name='站点名称', max_length=32)
    site_title = models.CharField(verbose_name='站点标题', max_length=32)
    site_theme = models.CharField(verbose_name='站点样式', max_length=64)

    def __str__(self):
        return self.site_name


# 文章标签表
class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签名', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name


# 文章分类表
class Category(models.Model):
    name = models.CharField(verbose_name='文章分类名', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name


# 文章表
class Article(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=32)
    desc = models.CharField(verbose_name='文章摘要', max_length=255)
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)

    up_num = models.BigIntegerField(verbose_name='点赞数', default=0)
    down_num = models.BigIntegerField(verbose_name='点踩数', default=0)
    comment_num = models.BigIntegerField(verbose_name='评论数', default=0)

    blog = models.ForeignKey(to='Blog', null=True)
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag',
                                  through='Article2tag',
                                  through_fields=('article', 'tag')
                                  )

    def __str__(self):
        return self.title


# 文章标签第三张表
class Article2tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')


# 点赞点踩表
class Up_and_down(models.Model):
    user = models.ForeignKey(to='Userinfo')
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField()


# 文章评论表
class Comment(models.Model):
    user = models.ForeignKey(to='Userinfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    parent = models.ForeignKey(to='self', null=True)

    def __str__(self):
        return self.content
