import datetime as dt


def validated_post_walking_form(self, form):
    if form.cleaned_data['walk_date'].date() > dt.date.today():
        form.add_error('walk_date', 'Дата обхода еще не наступила')
    if not any([form.cleaned_data['planned'], form.cleaned_data['not_planned']]):
        form.add_error('planned', 'Выберите тип обхода (плановый/внеплановый/оба)')
    return form
