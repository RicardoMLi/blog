from django.http import JsonResponse
from django.views.generic import View

from .forms import CommentForm
from .models import Comment


class CommentView(View):

    def post(self, request):
        comment_form = CommentForm(request.POST)
        return_data = {}

        if comment_form.is_valid():
            to_user_id = request.POST.get('to_user_id', '')
            parent_id = request.POST.get('parent_id', '')
            comment = Comment()
            # 评论博客
            if to_user_id == '' and parent_id == '':
                comment.user = comment_form.cleaned_data['user']
                comment.blog = comment_form.cleaned_data['blog']
                comment.parent = None
                comment.content = comment_form.cleaned_data['comment']
                comment.save()
                return_data['status'] = 'success'
                return_data['msg'] = {
                    'parent_id': '',
                    'comment_tag_id': 'message_{0}'.format(comment.id)
                }
            # 评论评论
            else:
                parent_id = int(parent_id)
                comment.user = comment_form.cleaned_data['user']
                comment.blog = comment_form.cleaned_data['blog']
                comment.parent = Comment.objects.get(id=parent_id)
                comment.content = comment_form.cleaned_data['comment']
                comment.save()
                return_data['status'] = 'success'
                return_data['msg'] = {
                    'parent_id': parent_id,
                    'comment_tag_id': 'message_{0}'.format(parent_id)
                }

            return_data['msg'].update({
                'comment': comment_form.cleaned_data['comment'],
                'time': comment.created_time.timestamp(),
                'username': comment.user.username,
                'comment_id': comment.id,
                'user_id': comment.user.id,
            })
        else:
            return_data['status'] = 'fail'
            return_data['msg'] = '评论失败'

        return JsonResponse(return_data)



