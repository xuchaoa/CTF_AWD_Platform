import xadmin
from . import models


class NoticeDisplay(object):
    '''显示的字段'''
    list_display = ['notice_competition', 'notice_title', 'notice_content', 'notice_time']
    '''被检索的字段'''
    search_fields = ['notice_competition__competition_name', 'notice_content']
    '''设置过滤选项'''
    list_filter = ['notice_competition', 'notice_content', 'notice_time']
    '''每页显示条目数'''
    list_per_page = 10
    '''按id升序排列'''
    ordering = ['id']
    '''只读的字段'''
    readonly_fields = []
    '''被隐藏的字段(与只读矛盾)'''
    exclude = []


xadmin.site.register(models.NoticeProfile, NoticeDisplay)
