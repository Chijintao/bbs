from django.template import Library
from app01 import models
from django.db.models.functions import TruncMonth
from django.db.models import Count


register = Library()


@register.inclusion_tag('left_menu.html')
def left_menu(username):

    user_obj = models.Userinfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 文章分类
    category_list = models.Category.objects.filter(blog=blog).annotate(article_num=Count('article')).values('name',
                                                                                                            'article_num',
                                                                                                            'pk')
    # 文章标签
    tag_list = models.Tag.objects.filter(blog=blog).annotate(article_num=Count('article')).values('name', 'article_num',
                                                                                                  'pk')
    # 日期归档
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(article_num=Count('pk')).values('month', 'article_num')

    return locals()