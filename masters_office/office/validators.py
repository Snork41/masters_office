def validated_planned_field(self, form):
    """Проверяет тип обхода в записи журнала обходов."""
    if not any([form.cleaned_data['planned'], form.cleaned_data['not_planned']]):
        form.add_error(
            'planned', 'Выберите тип обхода (плановый/внеплановый/оба)'
        )
    return form
