from django.shortcuts import get_object_or_404, redirect

from .models import District


class CheckEnergyDistrictMixin:
    """Проверяет принадлежность юзера к требуемому энергорайону."""

    def get(self, request, *args, **kwargs):
        district_energy_district = get_object_or_404(District, slug=self.kwargs.get('slug_district')).energy_district
        user_energy_district = request.user.energy_district
        if user_energy_district != district_energy_district:
            return redirect('office:districts')
        return super().get(request, *args, **kwargs)


def validate_fields_post_repair(self, form):
    """Проверка полей заполненной формы записи
    в журнале ремонтых работ на соответствие требований."""
    if form.cleaned_data['date_start_working'] >= form.cleaned_data['date_end_working']:
        form.add_error(
            'date_end_working', 'Дата окончания работ не может быть раньше даты начала'
        )
    return form


def validate_fields_post_walking(self, form):
    """Проверка полей заполненной формы записи
    в журнале обходов на соответствие требований."""
    if not any([form.cleaned_data['planned'], form.cleaned_data['not_planned']]):
        form.add_error(
            'planned', 'Выберите тип обхода (плановый/внеплановый/оба)'
        )
    user_energy_district = self.request.user.energy_district
    for member in form.cleaned_data.get('members'):
        if member.energy_district != user_energy_district:
            form.add_error(
                'members', 'Персонал с другого энергорайона не доступен!'
            )
    if form.cleaned_data.get('district').energy_district != user_energy_district:
        form.add_error(
            'district', 'Тепловой источник другого энергорайона не доступен!'
        )
    return form


def get_filtered_energy_district(self, context):
    """Фильтруем для формы выбор источников и персонала при создании поста."""
    district = context['form'].fields.get('district')
    members = context['form'].fields.get('members')
    required_energy_district = self.request.user.energy_district
    if district:
        district.queryset = district.queryset.filter(energy_district=required_energy_district)
    if members:
        members.queryset = members.queryset.filter(energy_district=required_energy_district)
    return context
