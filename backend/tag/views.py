from django.http import JsonResponse
from django.views import View
from backend.authenticate import user_authenticate
from backend.utils import gen_failed_template, gen_success_template
from user.models import *


class TagCreateView(View):
    def post(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        name = request.POST.get('name')

        tag = Tags(name=name)
        tag.save()

        return JsonResponse(gen_success_template())


class TagSearchView(View):
    def get(self, request):
        token = request.COOKIES.get('session')
        auth, user = user_authenticate(token)
        if not auth:
            return JsonResponse(gen_failed_template(212))

        key_word = request.POST.get('key_word', '')
        tags = []
        for tag in Tags.objects.all():
            if key_word in tag.name:
                tags.append(tag.name)

        data = {
            'tags': tags,
        }

        return JsonResponse(gen_success_template(data=data))
