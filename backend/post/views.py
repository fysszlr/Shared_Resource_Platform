import numpy as np
import torch
from typing import Union
import os
from io import BytesIO

from django.http import JsonResponse
from django.views import View
from backend.authenticate import user_authenticate
from backend.utils import gen_failed_template, gen_success_template
from user.models import *

os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"

from text2vec import SentenceModel

model = SentenceModel("shibing624/text2vec-base-chinese")


def cos_sim(a: Union[torch.Tensor, np.ndarray], b: Union[torch.Tensor, np.ndarray]):
    # 参考https://github.com/shibing624/similarities/blob/main/similarities/utils/util.py
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))


class PostCreateView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        cost = int(request.POST.get('cost', 0))
        tags = request.POST.getlist('tags[]')
        title = request.POST.get('title')
        content = request.POST.get('content')
        bhpan_url = request.POST.get('bhpan_url')

        share = Shares(
            price=cost,
            headline=title,
            text=content,
            bhpanUrl=bhpan_url,
            creatorId=user.userId
        )
        now = []
        text_embeddings = model.encode(share.text)
        title_embeddings = model.encode(share.headline)
        now.append(np.array(text_embeddings))
        now.append(np.array(title_embeddings))
        now = np.mean(np.vstack(now), axis=0)
        buffer = BytesIO()
        np.save(buffer, now)
        share.vector = buffer.getvalue()
        buffer.close()
        share.save()

        shareId = share.shareId
        op = ShareOperators(
            shareId=shareId,
            userId=user.userId,
            type='Purchase',
        )
        op.save()
        for tagName in tags:
            tag = Tags.objects.get(name=tagName)
            tagId = tag.tagId
            shareTag = ShareTags(
                shareId=shareId,
                creatorId=user.userId,
                tagId=tagId
            )
            shareTag.save()

        return JsonResponse(gen_success_template())


class PostDetailView(View):
    def get(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)

        flag = False
        like = False
        dislike = False
        favourite = False
        if post.price == 0:
            flag = True

        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        ops = ShareOperators.objects.filter(userId=user.userId, shareId=post.shareId)
        for op in ops:
            if op.type == 'Purchase':
                flag = True
            if op.type == 'Like':
                like = True
            if op.type == 'Dislike':
                dislike = True
            if op.type == 'Favourite':
                favourite = True

        tags = []
        shareTags = ShareTags.objects.filter(shareId=post.shareId)
        for shareTag in shareTags:
            tag = Tags.objects.get(tagId=shareTag.tagId)
            tags.append(tag.name)
        favourites = 0
        likes = 0
        dislikes = 0
        ops = ShareOperators.objects.filter(shareId=post.shareId)
        for op in ops:
            if op.type == 'Like':
                likes += 1
            if op.type == 'Dislike':
                dislikes += 1
            if op.type == 'Favourite':
                favourites += 1
        data = {
            'post_id': post_id,
            'cost': post.price,
            'tags': tags,
            'title': post.headline,
            'content': post.text if paid else None,  # 如果未支付，content 应该为 None
            'bhpan_url': post.bhpanUrl,
            'paid': flag,
            'created_at': post.date,
            'favorites': favourites,
            'likes': likes,
            'dislikes': dislikes,
            'created_by': {
                'user_id': post.creatorId,
                'username': Users.objects.get(userId=post.creatorId).name,
                'avatar': Users.objects.get(userId=post.creatorId).avatar,
            },
            'like': like,
            'dislike': dislike,
            'favorite': favourite
        }

        return JsonResponse(gen_success_template(data=data))


class PostCommentDetailView(View):
    def get(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        page = int(request.POST.get('page', 1))
        per_page = int(request.POST.get('per_page', 30))
        post = Shares.objects.get(shareId=post_id)

        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        # todo: reply
        comments = []
        for comment in Comments.objects.filter(shareId=post.shareId, type='Comment'):
            likes = 0
            dislikes = 0
            like = False
            dislike = False
            for op in CommentOperators.objects.filter(commentId=comment.shareId):
                if op.type == 'Like':
                    likes += 1
                    if op.userId == user.userId:
                        like = True
                if op.type == 'Dislike':
                    dislikes += 1
                    if op.userId == user.userId:
                        dislike = True
            now = {
                'comment_id': comment.commentId,
                'content': comment.text,
                'created_at': comment.date,
                'likes': likes,
                'dislikes': dislikes,
                'parent_id': 0,
                'created_by': {
                    'user_id': comment.creatorId,
                    'username': Users.objects.get(userId=comment.creatorId).name,
                    'avatar': Users.objects.get(userId=comment.creatorId).avatar,
                },
                'like': like,
                'dislike': dislike
            }
            comments.append(now)

        total = len(comments)
        total_page = (total + per_page - 1) // per_page
        if page * per_page > total:
            comments = comments[page * per_page - per_page:]
        else:
            comments = comments[page * per_page - per_page:page * per_page]
        data = {
            'page': page if paid else None,
            'per_page': per_page if paid else None,
            'total': total if paid else None,
            'total_page': total_page if paid else None,
            'comments': comments if paid else None,
        }

        return JsonResponse(gen_success_template(data=data))


class PostCommentCreateView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        content = request.POST.get('content')
        parent_id = int(request.POST.get('parent_id', 0))
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        if parent_id == 0:
            comment = Comments(
                shareId=post.shareId,
                type='Comment',
                text=content,
                creatorId=user.userId
            )
        else:
            comment = Comments(
                shareId=post.shareId,
                replyId=parent_id,
                type='Reply',
                text=content,
                creatorId=user.userId
            )
        comment.save()

        return JsonResponse(gen_success_template())


class PostFavouriteView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        op = ShareOperators(
            shareId=post.shareId,
            userId=user.userId,
            type='Favourite',
        )
        op.save()
        return JsonResponse(gen_success_template())


class PostUnfavouriteView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        op = ShareOperators.objects.filter(
            shareId=post.shareId,
            userId=user.userId,
            type='Favourite',
        )
        op.delete()
        return JsonResponse(gen_success_template())


class PostLikeView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        op = ShareOperators(
            shareId=post.shareId,
            userId=user.userId,
            type='Like',
        )
        op.save()
        return JsonResponse(gen_success_template())


class PostUnlikeView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        op = ShareOperators.objects.filter(
            shareId=post.shareId,
            userId=user.userId,
            type='Like',
        )
        op.delete()
        return JsonResponse(gen_success_template())


class PostDislikeView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        op = ShareOperators(
            shareId=post.shareId,
            userId=user.userId,
            type='Dislike',
        )
        op.save()
        return JsonResponse(gen_success_template())


class PostUndislikeView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        paid = False
        for op in ShareOperators.objects.filter(shareId=post.shareId, userId=user.userId):
            if op.type == 'Purchase':
                paid = True
        if post.price == 0:
            paid = True
        if user.status != 'User':
            paid = True

        if not paid:
            return gen_failed_template(500)

        op = ShareOperators.objects.filter(
            shareId=post.shareId,
            userId=user.userId,
            type='Dislike',
        )
        op.delete()
        return JsonResponse(gen_success_template())


class PostSearchView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        page = int(request.GET.get('page', '1'))
        per_page = int(request.GET.get('per_page', '30'))
        tagNames = request.GET.getlist('tags[]')
        pay = request.GET.get('pay', None)
        sort_by = int(request.GET.get('sort_by', 0))
        key_word = request.GET.get('key_word')
        if not key_word:
            key_word = ''
        max_length = int(request.GET.get('max_length', '30'))

        shares = []
        for share in Shares.objects.all():
            if key_word in share.headline or key_word in share.text:
                shares.append(share)

        tags = []
        if tagNames:
            for tagName in tagNames:
                tag = Tags.objects.get(name=tagName)
                tags.append(tag.tagId)
        newShares = []
        for share in shares:
            flag = False
            for tag in tags:
                if ShareTags.objects.filter(shareId=share.shareId, tagId=tag).exists():
                    flag = True
                    break
            if len(tags) == 0:
                flag = True
            if (flag):
                newShares.append(share)
        shares = newShares

        # pay
        if pay != None:
            if pay == 'true':
                newShares = []
                for share in shares:
                    if share.price != 0:
                        newShares.append(share)
                shares = newShares
            else:
                newShares = []
                for share in shares:
                    if share.price == 0:
                        newShares.append(share)
                shares = newShares

        # maxlength
        newShares = []
        for share in shares:
            if len(share.headline) <= max_length:
                newShares.append(share)
        shares = newShares

        # sort
        for share in shares:
            share.like = len(ShareOperators.objects.filter(
                shareId=share.shareId,
                type='Like',
            ))
            share.dislike = len(ShareOperators.objects.filter(
                shareId=share.shareId,
                type='Dislike',
            ))
            share.favourite = len(ShareOperators.objects.filter(
                shareId=share.shareId,
                type='Favourite',
            ))
            share.save()

        if sort_by == 0:
            sos = ShareOperators.objects.filter(userId=user.userId)
            if len(sos) != 0:
                simi = []
                target = []
                for so in sos:
                    share = Shares.objects.get(shareId=so.shareId)
                    buffer = BytesIO(share.vector)
                    now = np.load(buffer, allow_pickle=True)
                    buffer.close()
                    target.append(now)
                target = np.mean(np.vstack(target), axis=0)
                for share in shares:
                    buffer = BytesIO(share.vector)
                    now = np.load(buffer, allow_pickle=True)
                    buffer.close()
                    simi.append({
                        'id': share.shareId,
                        'cos': cos_sim(target, now)
                    })
                simi = sorted(simi, key=lambda x: x['cos'], reverse=True)
                shares = [Shares.objects.get(shareId=it['id']) for it in simi]

        if sort_by == 1:
            shares.sort(key=lambda share: share.like, reverse=True)
        if sort_by == 2:
            shares.sort(key=lambda share: share.date, reverse=True)
        if sort_by == 3:
            # todo: do something
            pass
        if sort_by == 4:
            shares.sort(key=lambda share: share.favourite, reverse=True)

        total = len(shares)
        total_page = (total + per_page - 1) // per_page
        if total < per_page * page:
            shares = shares[page * per_page - per_page:]
        else:
            shares = shares[page * per_page - per_page:page * per_page]

        posts = []
        for share in shares:
            tags = [Tags.objects.get(tagId=shareTag.tagId).name for shareTag in
                    ShareTags.objects.filter(shareId=share.shareId)]
            now = {
                'post_id': share.shareId,
                # 'post_url': ,
                'title': share.headline,
                'created_by': {
                    'username': Users.objects.get(userId=share.creatorId).name,
                    'user_id': share.creatorId,
                    'avatar': Users.objects.get(userId=share.creatorId).avatar,
                },
                'created_at': share.date,
                'likes': share.like,
                'dislikes': share.dislike,
                'favorites': share.favourite,
                'cost': share.price,  # 免费为0
                'tags': tags,
                'profile': (share.text[:15] + '...') if len(share.text) > 15 else share.text,
                'comment': len(Comments.objects.filter(shareId=share.shareId)),
            }
            posts.append(now)
        data = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_page': total_page,
            'posts': posts
        }

        return JsonResponse(gen_success_template(data=data))


class PostOwnView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        posts = []
        total = len(Shares.objects.filter(creatorId=user.userId))
        for share in Shares.objects.filter(creatorId=user.userId):
            share.like = len(ShareOperators.objects.filter(
                shareId=share.shareId,
                type='Like',
            ))
            share.dislike = len(ShareOperators.objects.filter(
                shareId=share.shareId,
                type='Dislike',
            ))
            share.favorite = len(ShareOperators.objects.filter(
                shareId=share.shareId,
                type='Favourite',
            ))
            share.save()
            now = {
                'post_id': share.shareId,
                # 'post_url': ,
                'title': share.headline,
                'created_at': share.date,
                'likes': share.like,
                'dislikes': share.dislike,
                'favorites': share.favourite,
                'cost': share.price
            }
            posts.append(now)

        return JsonResponse(gen_success_template(data={
            'total': total,
            'posts': posts
        }))


class PostChangeView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        if post.creatorId != user.userId and user.status == 'User':
            return JsonResponse(gen_failed_template(500))

        cost = int(request.POST.get('cost', '-1'))
        tags = request.POST.getlist('tags[]')
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        bhpan_url = request.POST.get('bhpan_url', None)

        if cost != -1:
            post.price = cost
        tmp = ShareTags.objects.filter(shareId=post_id)
        tmp.delete()
        for tag_name in tags:
            tag = Tags.objects.get(name=tag_name)
            shareTags = ShareTags(
                shareId=post_id,
                tagId=tag.tagId,
            )
            shareTags.save()
        if title != None:
            post.headline = title
        if content != None:
            post.text = content
        if bhpan_url != None:
            post.bhpanUrl = bhpan_url
        now = []
        text_embeddings = model.encode(post.text)
        title_embeddings = model.encode(post.headline)
        now.append(np.array(text_embeddings))
        now.append(np.array(title_embeddings))
        now = np.mean(np.vstack(now), axis=0)
        buffer = BytesIO()
        np.save(buffer, now)
        post.vector = buffer.getvalue()
        buffer.close()
        post.save()
        return JsonResponse(gen_success_template())


class PostDeleteView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))
        if user.status != 'Administrator' and user.status != 'Root':
            return JsonResponse(gen_failed_template(214))

        post_id = request.POST.get('post_id', None)
        share = Shares.objects.get(shareId=post_id)
        share.delete()

        return JsonResponse(gen_success_template())


class PostPayView(View):
    def post(self, request, post_id):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        post = Shares.objects.get(shareId=post_id)
        if user.coin > post.price:
            op = ShareOperators(
                shareId=post.shareId,
                userId=user.userId,
                type='Purchase'
            )
            op.save()
            user.coin -= post.price
            Users.objects.get(userId=post.creatorId).coin += post.price
            user.save()
            return JsonResponse(gen_success_template())
        else:
            return JsonResponse(gen_failed_template(601))


class PostNewView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        everything = []
        everything.extend(Shares.objects.all())
        everything.extend(Rewards.objects.all())

        everything = sorted(everything, key=lambda k: k.date, reverse=True)[:5]

        data = []
        for it in everything:
            if isinstance(it, Shares):
                now = {
                    'title': it.headline,
                    'category': 0,
                    'cost': it.price,
                    'username': Users.objects.get(userId=it.creatorId).name,
                }
            else:
                now = {
                    'title': it.headline,
                    'category': 1,
                    'cost': it.reward,
                    'username': Users.objects.get(userId=it.creatorId).name,
                }
            data.append(now)

        return JsonResponse(gen_success_template(data=data))
