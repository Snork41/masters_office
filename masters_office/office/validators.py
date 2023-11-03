from django.shortcuts import get_object_or_404, redirect

from .models import District


def validated_planned_field(self, form):
    """Проверяет тип обхода в записи журнала обходов."""
    if not any([form.cleaned_data['planned'], form.cleaned_data['not_planned']]):
        form.add_error(
            'planned', 'Выберите тип обхода (плановый/внеплановый/оба)'
        )
    return form


class CheckEnergyDistrictMixin:
    """Проверяет принадлежность юзера к требуемому энергорайону."""

    def get(self, request, *args, **kwargs):
        district_energy_district = get_object_or_404(District, slug=self.kwargs.get('slug_district')).energy_district
        user_energy_district = request.user.energy_district
        if user_energy_district != district_energy_district:
            return redirect('office:districts')
        return super().get(request, *args, **kwargs)
