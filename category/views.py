from django.views import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from group.models import Group
from category.models import Category
from feed_app.services import get_error_message
from extra.forms import CategoryForm


class AdminCategoriesView(View):
    @staticmethod
    def get(request, lang):

        groups = Group.get_all()

        return TemplateResponse(request, 'categories.html', {
            'title': 'カテゴリー | FEED App 管理',
            'groups': groups,
            'lang': lang,
        })


class AdminCategoryView(View):
    @staticmethod
    def get(request, lang, category_id):

        category_model = Category()

        category = category_model.get_by_id(category_id)

        groups = Group.get_all()

        if category is None:
            raise Http404

        title = category.name_ja

        return TemplateResponse(request, 'category.html', {
            'title': title + ' | カテゴリー | FEED App 管理',
            'category': category,
            'groups': groups,
            'error_messages': {},
            'form_data': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang, category_id):

        category_model = Category()
        category = category_model.get_by_id(category_id)
        groups = Group.get_all()
        form = CategoryForm(request.POST)

        if category is None:
            return HttpResponseRedirect(
                '/{}/admin/categories'.format(lang))

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                category_model.edit_category(category_id, {
                    'name_ja': form.cleaned_data.get('name_ja'),
                    'name_en': form.cleaned_data.get('name_en'),
                    'image_url': form.cleaned_data.get('image_url'),
                    'order': form.cleaned_data.get('order'),
                    'group': form.cleaned_data.get('group'),
                })

                return HttpResponseRedirect(
                    '/{}/admin/categories'.format(lang))

            except:
                pass

        title = category.name_ja

        return TemplateResponse(request, 'category.html', {
                'title': title + ' | カテゴリー | FEED App 管理',
                'category': category,
                'groups': groups,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminCategoryCreateView(View):
    @staticmethod
    def get(request, lang):

        groups = Group.get_all()

        return TemplateResponse(request, 'category_create.html', {
            'title': '新規投稿 | カテゴリー | FEED App 管理',
            'groups': groups,
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang):

        form = CategoryForm(request.POST)
        category_model = Category()

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                category_model.create_category({
                    'name_ja': form.cleaned_data.get('name_ja'),
                    'name_en': form.cleaned_data.get('name_en'),
                    'image_url': form.cleaned_data.get('image_url'),
                    'order': form.cleaned_data.get('order'),
                    'group': form.cleaned_data.get('group'),
                })

                return HttpResponseRedirect(
                    '/{}/admin/categories'.format(lang))

            except:
                pass

        groups = Group.get_all()

        return TemplateResponse(
            request, 'category_create.html', {
                'title': '新規投稿 | カテゴリー | FEED App 管理',
                'groups': groups,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminCategoryDeleteView(View):
    @staticmethod
    def post(request, lang, category_id):
        category_model = Category()
        category = category_model.get_by_id(category_id)
        groups = Group.get_all()
        try:
            if category.video_set.all().count() != 0:
                category_model.delete_category(category_id)

            return HttpResponseRedirect('/{}/admin/categories'.format(lang))

        except:
            pass

        title = category.name_ja

        return TemplateResponse(request, 'category.html', {
                'title': title + ' | カテゴリー | FEED App 管理',
                'category': category,
                'groups': groups,
                'form_data': {},
                'error_messages': {'delete': 'invalid'},
                'lang': lang,
            })
