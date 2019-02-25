import xadmin
from xadmin import views

from .models import Profile, Skill


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '博客后台管理系统'
    site_footer = '我的博客'
    menu_style = 'accordion'


class SkillAdmin(object):
    list_display = ['name', 'master_rate']
    search_fields = ['name', 'master_rate']
    list_filter = ['name', 'master_rate']


class ProfileAdmin(object):
    list_display = ['name', 'desc', 'skill', 'address', 'occupation', 'company']
    search_fields = ['name', 'desc', 'skill', 'address', 'occupation', 'company']
    list_filter = ['name', 'desc', 'skill', 'address', 'occupation', 'company']


xadmin.site.register(Skill, SkillAdmin)
xadmin.site.register(Profile, ProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

