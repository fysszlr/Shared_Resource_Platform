import math

from django.http import JsonResponse
from django.views import View
from backend.authenticate import user_authenticate
from backend.utils import gen_failed_template, gen_success_template
from user.models import *


class NotificationUnreadView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return gen_failed_template(212)

        depth = int(request.GET.get('depth', '99'))
        tmp_ids = MessageUsers.objects.filter(userId=user.userId).values_list('messageId', flat=True)
        messages = Messages.objects.filter(messageId__in=tmp_ids, read=False)

        not_read = len(messages)
        list = []
        for message in messages[:depth]:
            if message.type == 0:
                notice = Notices.objects.get(message.noticeId)
                list.append({"message": {
                    "id": message.messageId,
                    "type": message.type,
                    "content": notice.text,
                    "url": notice.url,
                    "notified": notice.date
                }})
            elif message.type in [1, 2]:
                share = Shares.objects.get(message.shareId)
                list.append({"message": {
                    "id": message.messageId,
                    "type": message.type,
                    "content": share.text,
                    "url": share.url,
                    "notified": share.date
                }})
            elif message.type in [3, 4]:
                reward = Rewards.objects.get(message.rewardId)
                list.append({"message": {
                    "id": message.messageId,
                    "type": message.type,
                    "content": reward.text,
                    "url": reward.url,
                    "notified": reward.date
                }})
        ret_data = {
            "not_read": not_read,
            "messages": list,
        }
        return JsonResponse(gen_success_template(data=ret_data))


class NotificationSearchView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return gen_failed_template(212)

        if "key_word" in request.GET:
            try:
                tag = Tags.objects.get(name=request.GET["key_word"])
            except Tags.DoesNotExist:
                return gen_failed_template(701)
            tagIds = [tag.tagId]
        else:
            tagIds = [tag.tagId for tag in Tags.objects.all()]

        tmp_ids = MessageUsers.objects.filter(userId=user.userId).values_list('messageId', flat=True)
        messages = Messages.objects.filter(messageId__in=tmp_ids, read=False)
        tmp_messages = []
        for message in messages:
            if message.type == 0:
                notice = Notices.objects.get(message.noticeId)
                for noticeTag in NoticeTags.objects.all():
                    if noticeTag.noticeId == notice.noticeId and noticeTag.tagId in tagIds:
                        tmp_messages.append(message)
            elif message.type in [1, 2]:
                share = Shares.objects.get(message.shareId)
                for shareTag in ShareTags.objects.all():
                    if shareTag.shareId == share.shareId and shareTag.tagId in tagIds:
                        tmp_messages.append(message)
            elif message.type in [3, 4]:
                reward = Rewards.objects.get(message.rewardId)
                for rewardTag in RewardTags.objects.all():
                    if rewardTag.rewardId == reward.rewardId and rewardTag.tagId in tagIds:
                        tmp_messages.append(message)
        messages = tmp_messages

        if "status" in request.GET:
            status = request.GET["status"]
            messages = Messages.objects.filter(read=status)
        if "type" in request.GET:
            messages = messages.filter(type__in=request.GET["type"])

        page = int(request.GET.get("page", '1'))
        per_page = int(request.GET.get("per_page", '15'))

        total = len(messages)
        total_page = math.ceil(total / per_page)
        messages = messages[page * per_page - per_page:page * per_page]
        data = {
            "total": total,
            "total_page": total_page,
            "page": page,
            "per_page": per_page,
        }
        list = []
        for message in messages:
            if message.type == 0:
                notice = Notices.objects.get(message.noticeId)
                list.append({"message": {
                    "id": message.noticeId,
                    "type": message.type,
                    "status": message.read,
                    "content": notice.text,
                    "url": notice.url,
                    "notified": notice.date
                }})
            elif message.type in [1, 2]:
                share = Shares.objects.get(message.shareId)
                list.append({"message": {
                    "id": message.shareId,
                    "type": message.type,
                    "status": message.read,
                    "content": share.text,
                    "url": share.url,
                    "notified": share.date
                }})
            elif message.type in [3, 4]:
                reward = Rewards.objects.get(message.rewardId)
                list.append({"message": {
                    "id": message.rewardId,
                    "type": message.type,
                    "status": message.read,
                    "content": reward.text,
                    "url": reward.url,
                    "notified": reward.date
                }})
        data["messages"] = list
        return JsonResponse(gen_success_template(data=data))


class NotificationDetailView(View):
    def get(self, request, notificationId):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return gen_failed_template(212)

        try:
            message = Messages.objects.get(messageId=notificationId)
        except Messages.DoesNotExist:
            return gen_failed_template(301)

        if message.type == 0:
            notice = Notices.objects.get(message.noticeId)
            data = {
                "type": message.type,
                "content": notice.text,
                "url": notice.url,
                "notified": notice.date
            }
        elif message.type in [1, 2]:
            share = Shares.objects.get(message.shareId)
            data = {
                "type": message.type,
                "content": share.text,
                "url": share.url,
                "notified": share.date
            }
        elif message.type in [3, 4]:
            reward = Rewards.objects.get(message.rewardId)
            data = {
                "type": message.type,
                "content": reward.text,
                "url": reward.url,
                "notified": reward.date
            }
        else:
            return gen_failed_template(300)

        return gen_success_template(data=data)


class NotificationReadAllView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return gen_failed_template(212)

        messageIds = MessageUsers.objects.filter(userId=user.userId).values_list('messageId', flat=True)
        for message in Messages.objects.filter(messageId__in=messageIds):
            message.read = True
            message.save()

        return gen_success_template()
