from django import forms
from feed_app.validator import *
from django.forms.widgets import RadioSelect
from video.models import Video
from introduction.models import Introduction, Title
from category.models import Category
from topic.models import Topic
from group.models import Group


STATUS_CHOICES = [
    (2, '下書き'),
    (3, '非公開'),
    (1, '公開')]


class StatusForm(forms.Form):
    status = forms.ChoiceField(widget=RadioSelect,
                               choices=STATUS_CHOICES,
                               error_messages=ERROR_MESSAGES)


class IntroductionForm(forms.Form):
    name = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    body = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    thumbnail_url = forms.CharField(required=True,
                                    error_messages=ERROR_MESSAGES)
    titles = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Title.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Video.get_all()],
        error_messages = ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)


class VideoForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    body = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    youtube_id = forms.CharField(required=True,
                                 error_messages=ERROR_MESSAGES)
    pickup = forms.BooleanField(required=False)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    introductions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Introduction.get_all()],
        error_messages=ERROR_MESSAGES)
    topics = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Topic.get_all()],
        error_messages=ERROR_MESSAGES)
    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Category.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Video.get_all()],
        error_messages=ERROR_MESSAGES)


class TopicForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    body = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    image_url = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    event_url = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Video.get_all()],
        error_messages=ERROR_MESSAGES)


class TitleForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    introductions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Introduction.get_all()],
        error_messages=ERROR_MESSAGES)


class IntroductionEnForm(forms.Form):
    name = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    body = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    thumbnail_url = forms.CharField(required=True,
                                    error_messages=ERROR_MESSAGES)
    titles = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Title.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Video.get_all()],
        error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)


class VideoEnForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    body = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    youtube_id = forms.CharField(required=True,
                                 error_messages=ERROR_MESSAGES)
    pickup = forms.BooleanField(required=False)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    introductions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Introduction.get_all()],
        error_messages=ERROR_MESSAGES)
    topics = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Topic.get_all()],
        error_messages=ERROR_MESSAGES)
    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Category.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Video.get_all()],
        error_messages=ERROR_MESSAGES)


class TopicEnForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    body = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    image_url = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    event_url = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Video.get_all()],
        error_messages=ERROR_MESSAGES)


class TitleEnForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    introductions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Introduction.get_all()],
        error_messages=ERROR_MESSAGES)


class CategoryForm(forms.Form):
    name_ja = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
    name_en = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
    image_url = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
    order = forms.IntegerField(required=True, error_messages=ERROR_MESSAGES)
    group = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=lambda: [(v.id, v.id) for v in Group.get_all()],
        error_messages=ERROR_MESSAGES)


class GroupForm(forms.Form):
    name = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
