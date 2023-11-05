import datetime as dt
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.validators import MaxValueValidator
import os

from .models import PostWalking, Personal, Resolution, PostRepairWork
from .utils import add_number_post
from masters_office.settings import BASE_DIR


class PostWalkingForm(forms.ModelForm):

    walk_date = forms.DateField(
        label='Дата обхода',
        widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        validators=[MaxValueValidator(dt.date.today(), message='Дата обхода еще не наступила')]
    )
    fix_date = forms.DateField(
        label='Дата устранения замечания',
        help_text='При отсутствии замечаний не заполняется',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'min': dt.date.today()})
    )
    planned = forms.BooleanField(
        error_messages={'planned': 'ererer'},
        label='Плановый',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'id': 'btn-check-planned-outlined', 'type': 'checkbox', 'class': 'btn-check'})
    )
    not_planned = forms.BooleanField(
        label='Внеплановый',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'btn-check-not-planned-outlined', 'type': 'checkbox', 'class': 'btn-check'})
    )
    members = forms.ModelMultipleChoiceField(
        label='Члены бригады',
        queryset=Personal.objects.filter(position__walker=True),
        widget=FilteredSelectMultiple(
            verbose_name='Члены бригады',
            is_stacked=False
        ),
    )
    is_deleted = forms.BooleanField(
        label='Пометить запись на удаление',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'btn-check-deleted-outlined', 'type': 'checkbox', 'class': 'btn-check'})
    )

    class Meta:
        model = PostWalking
        fields = (
            'district',
            'planned',
            'not_planned',
            'walk_date',
            'members',
            'task',
            'text',
            'plan',
            'fix_date',
            'transfer',
            'is_deleted',
        )

    class Media:
        css = {
            'all': [os.path.join(BASE_DIR, 'static/css/select_multiple.css')],
        }
        js = ('/admin/jsi18n',)

    def save(self, username=None, commit=True, *args, **kwargs):
        obj = super().save(commit=False, *args, **kwargs)
        return add_number_post(self, obj, PostWalking, username, commit, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        for field in ['district', 'walk_date', 'task', 'text', 'plan', 'fix_date', 'transfer']:
            if field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'focus-ring focus-ring-dark border'})
        if self.instance.time_create and 'district' in self.fields:
            self.fields['district'].disabled = True


class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': '5', 'cols': '60', 'style': 'max-width: 100%'})
        }


class PostRepairWorkForm(forms.ModelForm):

    class Meta:
        model = PostRepairWork
        fields = (
            'district',
            'order',
            'number_order',
            'adress',
            'description',
            'date_start_working',
            'date_end_working',
            'is_deleted',
        )
        widgets = {
            'date_start_working': forms.DateTimeInput(format=('%Y-%m-%d'), attrs={'type': 'datetime-local'}),
            'date_end_working': forms.DateTimeInput(format=('%Y-%m-%d'), attrs={'type': 'datetime-local'}),
        }

    def save(self, username=None, *args, commit=True, **kwargs):
        obj = super().save(commit=False, *args, **kwargs)
        return add_number_post(self, obj, PostRepairWork, username, commit, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'focus-ring focus-ring-dark border'})
