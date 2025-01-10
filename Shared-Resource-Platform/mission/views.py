from django.http import JsonResponse
from django.views import View
from backend.authenticate import user_authenticate
from backend.utils import gen_failed_template, gen_success_template
from user.models import *


class MissionCreateView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        commission = int(request.POST.get('commission', '0'))
        tags = request.POST.getlist('tags[]')
        title = request.POST.get('title')
        content = request.POST.get('content')

        reward = Rewards(
            headline=title,
            text=content,
            profile=content[:50],
            reward=commission,
            creatorId=user.userId,
        )
        reward.save()

        for tag_name in tags:
            tag = Tags.objects.get(name=tag_name)
            rewardTag = RewardTags(
                rewardId=reward.rewardId,
                tagId=tag.tagId,
            )
            rewardTag.save()

        return JsonResponse(gen_success_template())


class MissionDetailView(View):
    def get(self, request, mission_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        reward = Rewards.objects.get(rewardId=mission_id)
        tags = []
        for tag in RewardTags.objects.filter(rewardId=reward.rewardId):
            tags.append(Tags.objects.get(tagId=tag.tagId).name)
        data = {
            'mission_id': reward.rewardId,
            # 'url':"",
            'open': not reward.close,
            'commission': reward.reward,
            'tags': tags,
            'title': reward.headline,
            'content': reward.text,
            'created_at': reward.date,
            'created_by': {
                'username': Users.objects.get(userId=reward.creatorId).name,
                'avatar': str(Users.objects.get(userId=reward.creatorId).avatar),
                'user_id': reward.creatorId,
            }
        }

        return JsonResponse(gen_success_template(data=data))


class MissionSubmitView(View):
    def post(self, request, mission_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        profile = request.POST.get('profile')
        bhpan_url = request.POST.get('bhpan_url')
        reward = Rewards.objects.get(rewardId=mission_id)
        if user.userId == reward.creatorId:
            return JsonResponse(gen_success_template())
        answer = Answers(
            rewardId=reward.rewardId,
            creatorId=user.userId,
            text=profile,
            resource_link=bhpan_url
        )
        answer.save()

        return JsonResponse(gen_success_template())


class MissionAnswerView(View):
    def get(self, request, mission_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        reward = Rewards.objects.get(rewardId=mission_id)
        page = int(request.POST.get('page', '1'))
        per_page = int(request.POST.get('per_page', '15'))

        submits = []
        for answer in Answers.objects.filter(rewardId=reward.rewardId):
            now = {
                'submit_id': answer.answerId,
                'profile': answer.text,
                'created_at': answer.date,
                'created_by': {
                    'username': Users.objects.get(userId=answer.creatorId).name,
                    'avatar': str(Users.objects.get(userId=answer.creatorId).avatar),
                    'user_id': answer.creatorId,
                },
                'bhpan_url': answer.resource_link,
            }
            submits.append(now)

        total = len(submits)
        total_page = (total + per_page - 1) // per_page
        if total < per_page * page:
            submits = submits[page * per_page - per_page:]
        else:
            submits = submits[page * per_page - per_page: per_page * page]

        data = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_page': total_page,
            'submits': submits,
        }

        return JsonResponse(gen_success_template(data=data))


class MissionCloseView(View):
    def post(self, request, mission_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        reward = Rewards.objects.get(rewardId=mission_id)
        accepted = request.POST.get('accepted')

        reward.answerId = accepted
        reward.close = True
        reward.url = Answers.objects.get(answerId=accepted).resource_link
        reward.save()

        return JsonResponse(gen_success_template())


class MissionSearchView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        page = int(request.GET.get('page', '30'))
        per_page = int(request.GET.get('per_page', '1'))
        tags = request.GET.getlist('tags[]')
        status = request.GET.get('status', None)
        sort_by = int(request.GET.get('sort_by', 0))
        key_word = request.GET.get('key_word', '')
        max_length = int(request.GET.get('max_length', '30'))

        posts = []
        for reward in Rewards.objects.filter(close=False):
            if len(tags) != 0:
                flag = False
                for rewardTag in RewardTags.objects.filter(rewardId=reward.rewardId):
                    tag = Tags.objects.get(tagId=rewardTag.tagId)
                    for tag_name in tags:
                        if tag.name == tag_name:
                            flag = True
                            break
                if not flag:
                    continue
            if status != None:
                if status == 'true':
                    if reward.close:
                        continue
                else:
                    if not reward.close:
                        continue
            if key_word not in reward.text and key_word not in reward.headline:
                continue
            posts.append(reward)

        if sort_by == 0:
            import random
            random.shuffle(posts)
        if sort_by == 2:
            posts.sort(key=lambda post: post.date, reverse=True)
        if sort_by == 3:
            # todo: do something
            pass
        if sort_by == 4:
            posts.sort(key=lambda post: post.reward, reverse=True)

        total = len(posts)
        total_page = (total + per_page - 1) // per_page
        if total < per_page * page:
            posts = posts[page * per_page - per_page:]
        else:
            posts = posts[page * per_page - per_page: per_page * page]

        tmp = []
        for post in posts:
            tags = [Tags.objects.get(tagId=rewardTag.tagId).name for rewardTag in
                    RewardTags.objects.filter(rewardId=post.rewardId)]
            now = {
                'mission_id': post.rewardId,
                'title': post.headline,
                'created_at': post.date,
                'commission': post.reward,
                'tiny_content': (post.profile + '...') if len(post.profile) > max_length else post.profile,
                'created_by': {
                    'username': Users.objects.get(userId=post.creatorId).name,
                    'avatar': str(Users.objects.get(userId=post.creatorId).avatar),
                    'user_id': post.creatorId,
                },
                'tags': tags
            }
            tmp.append(now)

        data = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_page': total_page,
            'posts': tmp,
        }

        return JsonResponse(gen_success_template(data=data))


class MissionOwnView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        rewards = Rewards.objects.filter(creatorId=user.userId)
        total = len(rewards)
        tmp = []
        for post in rewards:
            tags = [Tags.objects.get(tagId=it.tagId).name for it in RewardTags.objects.filter(rewardId=post.rewardId)]
            now = {
                'mission': post.rewardId,
                'title': post.headline,
                'created_at': post.date,
                'commission': post.reward,
                'tiny_content': (post.profile + '...') if len(post.profile) > 50 else post.profile,
                'tags': tags
            }
            tmp.append(now)

        data = {
            'total': total,
            'posts': tmp,
        }

        return JsonResponse(gen_success_template(data=data))


class MissionDeleteView(View):
    def post(self, request, mission_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        reward = Rewards.objects.get(rewardId=mission_id)
        reward.delete()
        return JsonResponse(gen_success_template())


class MissionChangeView(View):
    def post(self, request, mission_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        reward = Rewards.objects.get(rewardId=mission_id)
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        tags = request.POST.getlist('tags[]')
        commssion = int(request.POST.get('commssion', '-1'))

        if title != None:
            reward.headline = title
        if content != None:
            reward.text = content
        if len(tags) > 0:
            old_tags = RewardTags.objects.filter(rewardId=reward.rewardId)
            old_tags.delete()
            for tag_name in tags:
                tag = Tags.objects.get(name=tag_name)
                rewardTag = RewardTags(
                    rewardId=reward.rewardId,
                    tagId=tag.tagId,
                )
                rewardTag.save()
        if commssion >= 0:
            reward.reward = commssion

        reward.save()
        return JsonResponse(gen_success_template())
