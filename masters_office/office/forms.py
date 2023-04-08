from django import forms

from .models import PostWalking, Personal


class PostWalkingForm(forms.ModelForm):
    class Meta:
        model = PostWalking
        fields = (
            'district',
            'planned',
            'not_planned',
            'pub_date',    
            'members',
            'task',
            'text',
            'plan',
            'resolution',
            'fix_date',
            'transfer',
        )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
   

    def save(self, username=None, *args, commit=True, **kwargs):
        """Сохранение записи с автоматической нумерацией, учитывая район."""

        obj = super().save(commit=False, *args, **kwargs)
        if not obj.number_post:
            most_recent = PostWalking.objects.filter(
                district=obj.district).order_by('-number_post').first()
            obj.number_post = most_recent.number_post + 1 if most_recent else 1
            if username:
                obj.author = username
        if commit:
            obj.save()
            self._save_m2m()
        return obj
