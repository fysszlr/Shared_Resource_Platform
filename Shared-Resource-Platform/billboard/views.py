import math

from django.http import JsonResponse
from django.views import View
from backend.authenticate import user_authenticate
from backend.utils import gen_failed_template, gen_success_template
from user.models import *


class BillboardIndexView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        page = int(request.GET.get('page', '1'))
        per_page = int(request.GET.get('per_page', '15'))
        max_length = int(request.GET.get('max_length', '30'))
        messages = Messages.objects.filter(userId=user.userId, read=False)

        message_list = []
        for message in messages:
            if message.type == 'Notice':
                noticeMessage = NoticeMessages.objects.get(messageId=message.messageId)
                notice = Notices.objects.get(noticeId=noticeMessage.noticeId)
                now = {
                    "id": notice.noticeId,
                    "content": notice.text,
                    "notified_at": notice.date,
                    "title": notice.title,
                }
                message_list.append(now)
            # todo:其它类型notice

        total = len(message_list)
        total_page = (total + per_page - 1) // per_page
        if total > page * per_page - per_page:
            message_list = message_list[page * per_page - per_page:]
        else:
            message_list = message_list[page * per_page - per_page: page * per_page]

        data = {
            "total": total,
            "total_page": total_page,
            "page": page,
            "per_page": per_page,
            "messages": message_list
        }

        return JsonResponse(gen_success_template(data=data))


class BillboardDetailView(View):
    def get(self, request, noticeId):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        notice = Notices.objects.get(noticeId=noticeId)
        data = {
            "content": notice.text,
            "notified_at": notice.date
        }
        return JsonResponse(gen_success_template(data=data))


class BillboardCreateView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        title = request.POST.get('title')
        content = request.POST.get('content')

        notice = Notices(title=title, text=content)
        notice.save()

        for user in Users.objects.all():
            message = Messages(
                userId=user.userId,
                type='Notice',
            )
            message.save()
            noticeMessage = NoticeMessages(
                messageId=message.messageId,
                noticeId=notice.noticeId,
            )
            noticeMessage.save()
        return JsonResponse(gen_success_template())


class BillboardModifyView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        id = int(request.POST.get('id'))
        title = request.POST.get('title')
        content = request.POST.get('content')

        notice = Notices.objects.get(noticeId=id)
        if title != "":
            notice.title = title
        if content == "":
            notice.text = content
        notice.save()

        return JsonResponse(gen_success_template())
