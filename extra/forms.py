from django import forms
from feed_app.validator import *
from django.forms.widgets import RadioSelect
from extra.models import Image
from video.models import Video, VideoEn
from introduction.models import Introduction, IntroductionEn, Title, TitleEn
from category.models import Category
from topic.models import Topic, TopicEn
from group.models import Group


STATUS_CHOICES = [
    (2, '下書き'),
    (3, '非公開'),
    (1, '公開')]


class StatusForm(forms.Form):
    status = forms.ChoiceField(widget=RadioSelect,
                               choices=STATUS_CHOICES,
                               error_messages=ERROR_MESSAGES)


class NewForm(forms.Form):
    new = forms.BooleanField(required=False,
                             error_messages=ERROR_MESSAGES)


class IntroductionForm(forms.Form):
    name = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    text = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    thumbnail = forms.CharField(required=True,
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


class VideoForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    text = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    youtube_id = forms.CharField(required=True,
                                 error_messages=ERROR_MESSAGES)
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
    post_type = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    new = forms.BooleanField(required=False,
                             error_messages=ERROR_MESSAGES)
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    text = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    url = forms.CharField(required=True,
                          error_messages=ERROR_MESSAGES)
    button_label = forms.CharField(required=True,
                                   error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    event_date = forms.DateTimeField(required=False,
                                     error_messages=ERROR_MESSAGES)
    thumbnail = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    images = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Image.get_all()],
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
    text = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    thumbnail = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    titles = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in TitleEn.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in VideoEn.get_all()],
        error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)


class VideoEnForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    text = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    youtube_id = forms.CharField(required=True,
                                 error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    introductions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in IntroductionEn.get_all()],
        error_messages=ERROR_MESSAGES)
    topics = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in TopicEn.get_all()],
        error_messages=ERROR_MESSAGES)
    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Category.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in VideoEn.get_all()],
        error_messages=ERROR_MESSAGES)


class TopicEnForm(forms.Form):
    post_type = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    new = forms.BooleanField(required=False,
                             error_messages=ERROR_MESSAGES)
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    text = forms.CharField(required=True,
                           error_messages=ERROR_MESSAGES)
    url = forms.CharField(required=True,
                          error_messages=ERROR_MESSAGES)
    button_label = forms.CharField(required=True,
                                   error_messages=ERROR_MESSAGES)
    published_at = forms.DateTimeField(required=True,
                                       error_messages=ERROR_MESSAGES)
    event_date = forms.DateTimeField(required=False,
                                     error_messages=ERROR_MESSAGES)
    thumbnail = forms.CharField(required=True,
                                error_messages=ERROR_MESSAGES)
    images = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in Image.get_all()],
        error_messages=ERROR_MESSAGES)
    videos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in VideoEn.get_all()],
        error_messages=ERROR_MESSAGES)


class TitleEnForm(forms.Form):
    title = forms.CharField(required=True,
                            error_messages=ERROR_MESSAGES)
    introductions = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(v.id, v.id) for v in IntroductionEn.get_all()],
        error_messages=ERROR_MESSAGES)


class CategoryForm(forms.Form):
    name_ja = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
    name_en = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
    image = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
    order = forms.IntegerField(required=True, error_messages=ERROR_MESSAGES)
    group = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=lambda: [(v.id, v.id) for v in Group.get_all()],
        error_messages=ERROR_MESSAGES)


class GroupForm(forms.Form):
    name = forms.CharField(required=True, error_messages=ERROR_MESSAGES)
