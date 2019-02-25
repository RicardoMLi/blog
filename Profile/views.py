from django.shortcuts import render
from django.views.generic import View

from Profile.models import Skill
from Category.models import Category


class AboutMeView(View):

    def get(self, request):
        context = {}
        parent_categories = Category.objects.filter(parent_id=None)
        skills = Skill.objects.all()
        context['parent_categories'] = parent_categories
        context['skills'] = skills
        context['name'] = '关于念旧'
        return render(request, 'profile/me.html', context)
