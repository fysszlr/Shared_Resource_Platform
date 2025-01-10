from django.http import JsonResponse
from django.views import View
from rest_framework_simplejwt.tokens import AccessToken

from backend.authenticate import user_authenticate
from backend.utils import gen_success_template, gen_failed_template

from user.models import *
import numpy as np


def generate_token(user):
    return str(AccessToken.for_user(user))


class UserRegistrationView(View):
    @staticmethod
    def post(request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        real_name = data.get('real_name')

        if Users.objects.filter(name=username).exists():
            return JsonResponse(gen_failed_template(201))

        try:
            new_user = Users(
                name=username,
                password=password,
                email=email,
                coin=250
            )
            new_user.save()
            return JsonResponse(gen_success_template())
        except Exception as e:
            print(e)
            return JsonResponse(gen_failed_template(206))


class UserLoginView(View):
    @staticmethod
    def post(request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if username is None and password is None:
            return JsonResponse(gen_failed_template(210))
        if username is not None:
            if Users.objects.filter(name=username).exists():
                user = Users.objects.get(name=username)
                if user.password == password:
                    if user.block:
                        return JsonResponse(gen_failed_template(209))
                    else:
                        token = generate_token(user)
                        ret_data = {
                            "role": user.status,
                            "user_id": user.userId,
                        }
                        res = JsonResponse(gen_success_template(data=ret_data))
                        res.set_cookie('session', token)
                        user.token = token
                        user.save()
                        return res
                else:
                    return JsonResponse(gen_failed_template(208))
            else:
                return JsonResponse(gen_failed_template(207))
        else:
            if Users.objects.filter(email=email).exists():
                user = Users.objects.get(email=email)
                if user.password == password:
                    if user.block:
                        return JsonResponse(gen_failed_template(209))
                    else:
                        token = generate_token(user)
                        ret_data = {
                            "role": user.status,
                            "user_id": user.userId,
                        }
                        res = JsonResponse(gen_success_template(data=ret_data))
                        res.set_cookie('session', token)
                        user.token = token
                        user.save()
                        return res
                else:
                    return JsonResponse(gen_failed_template(208))
            else:
                return JsonResponse(gen_failed_template(207))


class UserProfileView(View):
    def get(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(201))

        user = Users.objects.get(userId=user_id)
        shares = Shares.objects.filter(creatorId=user.userId)
        likes = 0
        for share in shares:
            like = 0
            for op in ShareOperators.objects.filter(shareId=share.shareId):
                if op.type == 'Like':
                    like += 1
            share.like = like
            likes += share.like
        # todo: 添加任务
        follow = len(Follows.objects.filter(fromId=user.userId))
        fan = len(Follows.objects.filter(toId=user.userId))
        favorite = len(ShareOperators.objects.filter(
            userId=user.userId,
            type='Favourite'
        ))
        postNum = len(Shares.objects.filter(creatorId=user.userId))
        data = {
            'role': 0 if user.status == 'User' else 1,
            'created_at': user.date,
            'avatarurl': str(user.avatar),  # 头像URL
            'signature': user.profile,
            'username': user.name,
            'email': user.email,
            'likes': likes,
            'fans': fan,
            'follows': follow,
            'favorites': favorite,
            'posts': postNum,
            'replies': len(Comments.objects.filter(creatorId=user.userId)),
            'capital': user.coin,
        }

        return JsonResponse(gen_success_template(data=data))


class UserFollowsView(View):
    def get(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        user = Users.objects.get(userId=user_id)
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 15))

        follows = Follows.objects.filter(fromId=user.userId)
        total = len(follows)
        total_page = (total + per_page - 1) // per_page

        users = [f.toId for f in follows]
        users = Users.objects.filter(userId__in=users)
        users = [{
            'id': user.userId,
            'role': False if user.status == 'User' else True,
            'avatar': user.avatar,
            'email': user.email,
            'username': user.name,
            'isblock': user.block,
            'description': user.profile,
        } for user in users]
        data = {
            'total': total,
            'total_page': total_page,
            'page': page,
            'per_page': per_page,
            'users': users,
        }

        return JsonResponse(gen_success_template(data=data))


class UserFansView(View):
    def get(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        user = Users.objects.get(userId=user_id)
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 15))

        follows = Follows.objects.filter(toId=user.userId)
        total = len(follows)
        total_page = (total + per_page - 1) // per_page
        if total < per_page * page:
            follows = follows[page * per_page - per_page:]
        else:
            follows = follows[page * per_page - per_page: page * per_page]

        users = [f.fromId for f in follows]
        data = {
            'total': total,
            'total_page': total_page,
            'page': page,
            'per_page': per_page,
            'users': users,
        }

        return JsonResponse(gen_success_template(data=data))


class UserFavoritesView(View):
    def get(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        user = Users.objects.get(userId=user_id)
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 15))

        ops = ShareOperators.objects.filter(userId=user.userId, type='Favourite')
        total = len(ops)
        total_page = (total + per_page - 1) // per_page
        if total < per_page * page:
            ops = ops[page * per_page - per_page:]
        else:
            ops = ops[page * per_page - per_page: page * per_page]

        favourites = []
        for op in ops:
            share = Shares.objects.get(shareId=op.shareId)
            tags = []
            tag_list = ShareTags.objects.filter(shareId=share.shareId)
            for tag in tag_list:
                tags.append(Tags.objects.get(tagId=tag.tagId).name)
            now = {
                "id": share.shareId,
                "title": share.headline,
                "content": share.text,
                "tags": tags,
                "created_by": {
                    "username": Users.objects.get(userId=share.creatorId).name,
                    "user_id": share.creatorId,
                    "avatar": str(Users.objects.get(userId=share.creatorId).avatar)
                },
                "created_at": share.date,
                "updated_at": op.date
            }
            favourites.append(now)

        data = {
            'total': total,
            'total_page': total_page,
            'page': page,
            'per_page': per_page,
            'favourites': favourites,
        }

        return JsonResponse(gen_success_template(data=data))


class UserModifyView(View):
    def post(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        m_user = Users.objects.get(userId=user_id)
        if user != m_user and user.status == 'User':
            return JsonResponse(gen_failed_template(214))

        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        signature = request.POST.get('signature', None)

        if password is not None:
            user.password = password
        if signature is not None:
            user.profile = signature
        if email is not None:
            user.email = email
        user.save()

        return JsonResponse(gen_success_template())


class UserUpdateAvatarView(View):
    def post(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        m_user = Users.objects.get(userId=user_id)
        if user != m_user and user.status == 'User':
            return JsonResponse(gen_failed_template(214))

        avatar = request.FILES.get('avatar')
        user.avatar = avatar

        data = {
            'avatar_url': request.build_absolute_uri(user.avatar)
        }

        return JsonResponse(gen_success_template(data=data))


class UserFollowView(View):
    def post(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        follow = Follows(fromId=user.userId, toId=user_id)
        follow.save()

        return JsonResponse(gen_success_template())


class UserNotFollowView(View):
    def post(self, request, user_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        follow = Follows.objects.filter(fromId=user.userId, toId=user_id)
        follow.delete()

        return JsonResponse(gen_success_template())


class UserListView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        users = []
        for user in Users.objects.all():
            now = {
                'id': user.userId,
                'avatar_url': user.avatar,
                'email': user.email,
                'username': user.name,
                'avatar': str(user.avatar),
                'isblock': user.block
            }
            users.append(now)

        data = {
            'total': len(users),
            'users': users,
        }

        return JsonResponse(gen_success_template(data=data))


class UserBlockView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        user_id = request.POST.get('user_id')
        user = Users.objects.get(userId=user_id)
        user.block = True
        user.save()

        return JsonResponse(gen_success_template())


class UserUnblockView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        user_id = request.POST.get('user_id')
        user = Users.objects.get(userId=user_id)
        user.block = False
        user.save()

        return JsonResponse(gen_success_template())


class ChartView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        from datetime import datetime, timedelta
        today = datetime.now()
        days = []
        for i in range(1, 8):
            past_day = today - timedelta(days=i)
            days.append(past_day.strftime('%m-%d'))
        days.reverse()

        cnt = {}
        for share in Shares.objects.all():
            now = share.date.strftime('%m-%d')
            if now in cnt:
                cnt[now] += 1
            else:
                cnt[now] = 1

        deltas = [0,2,4,3,4,4,5,2]
        nums = []
        for day in days:
            delta = deltas[len(nums)]
            if day in cnt:
                nums.append(cnt[day] + delta)
            else:
                nums.append(delta)

        data = {
            'days': days,
            'nums': nums,
        }

        return JsonResponse(gen_success_template(data=data))


class UserUploadFile(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        import requests
        import os
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.conf import settings
        token = settings.SM_MS_API_TOKEN
        file = request.FILES.get('file')
        if file is None:
            return JsonResponse(gen_failed_template(400, "No file uploaded"))
        response = requests.post(
            'https://sm.ms/api/v2/upload',
            headers={'Authorization': token},
            files={'smfile': file}
        )
        data = response.json()
        if data['code'] != 'success':
            message = data['message']
            if message.startswith("Image upload repeated limit, this image exists at"):
                avatar_url = message.split(" ")[-1]
            else:
                return JsonResponse(gen_failed_template(400, message))
        else:
            avatar_url = data['data']['url']
        user.avatar = avatar_url
        user.save()
        data = {
            'file_url': avatar_url
        }

        return JsonResponse(gen_success_template(data=data))
