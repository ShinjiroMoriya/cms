from feed_app.caches_manager import Cache
from django.views import View
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from group.models import Group
from group.serializers import GroupSerializer, GroupEnSerializer
from feed_app.services import get_error_message
from extra.forms import GroupForm


class GroupsView(View):
    @staticmethod
    def get(_, lang):
        if lang == 'ja':
            cached_groups = Cache.get('api_groups')
            if cached_groups is None:
                res = GroupSerializer(Group.get_all(), many=True).data
                Cache.set('api_groups', res)
            else:
                res = cached_groups

        elif lang == 'en':
            try:
                cached_groups_en = Cache.get('api_groups_en')
            except:
                cached_groups_en = None

            if cached_groups_en is None:
                res = GroupEnSerializer(Group.get_all(), many=True).data
                Cache.set('api_groups_en', res)
            else:
                res = cached_groups_en

        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class AdminGroupsView(View):
    @staticmethod
    def get(request, lang):

        groups = Group.get_all()

        return TemplateResponse(request, 'groups.html', {
            'title': 'グループ | FEED App 管理',
            'groups': groups,
            'lang': lang,
        })


class AdminGroupView(View):
    @staticmethod
    def get(request, lang, group_id):

        group = Group.get_by_id(group_id)

        if group is None:
            raise Http404

        title = group.name

        return TemplateResponse(request, 'group.html', {
            'title': title + ' | グループ | FEED App 管理',
            'group': group,
            'error_messages': {},
            'form_data': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang, group_id):
        group_model = Group()
        group = group_model.get_by_id(group_id)
        form = GroupForm(request.POST)

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                group_model.edit_group(group_id, {
                    'name': form.cleaned_data.get('name'),
                })

                return HttpResponseRedirect(
                    request.META.get('HTTP_REFERER', '/'))

            except:
                pass

        title = group.name

        return TemplateResponse(request, 'group.html', {
                'title': title + ' | グループ | FEED App 管理',
                'group': group,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminGroupCreateView(View):
    @staticmethod
    def get(request, lang):
        return TemplateResponse(request, 'group_create.html', {
            'title': '新規投稿 | グループ | FEED App 管理',
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang):

        form = GroupForm(request.POST)
        group_model = Group()

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                group_model.create_group({
                    'name': form.cleaned_data.get('name'),
                })

                return HttpResponseRedirect('/{}/admin/groups'.format(lang))

            except:
                pass

        return TemplateResponse(
            request, 'group_create.html', {
                'title': '新規投稿 | グループ | FEED App 管理',
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminGroupDeleteView(View):
    @staticmethod
    def post(request, lang, group_id):
        group_model = Group()
        group = group_model.get_by_id(group_id)
        try:
            if group.categories.all().count() != 0:
                group_model.delete_group(group_id)

            return HttpResponseRedirect('/{}/admin/groups'.format(lang))

        except:
            pass

        title = group.name

        return TemplateResponse(request, 'group.html', {
            'title': title + ' | グループ | FEED App 管理',
            'group': group,
            'form_data': {},
            'error_messages': {'delete': 'invalid'},
            'lang': lang,
        })
