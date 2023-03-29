from django.contrib import admin

from .forms import PostWalkingForm
from .models import Journal, PostWalking, Personal, District, Position, EnergyDistrict, Brigade


class PostWalkingAdmin(admin.ModelAdmin):
    form = PostWalkingForm
    list_display = (
        'pk',
        'number_post',
        'district',
        'planned',
        'not_planned',
        'pub_date',
        'task',
        'text_for_display',
        'author',
    )
    fields = (
        'author',
        'district',
        ('time_create', 'time_update'),
        ('planned', 'not_planned'),
        'pub_date',    
        'members',
        'task',
        'text',
        'plan',
        'resolution',
        'fix_date',
        'transfer',
    )
    list_display_links = ('number_post', 'task')
    search_fields = ('text', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    save_on_top = True
    readonly_fields = ('time_create', 'time_update', 'number_post')
    filter_horizontal = ('members',)
    list_per_page = 20


class JournalAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'description',
        'slug',
    )
    list_display_links = ('title',)
    empty_value_display = '-пусто-'


class BrigadeAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'master',
        'brigadier',
    )
    # list_display_links = ('',)
    filter_horizontal = ('members',)
    empty_value_display = '-пусто-'


class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'master',
        'slug',
    )
    list_editable = ('master',)
    # search_fields = ('title', 'master')
    # list_filter = ('master',)
    list_display_links = ('title',)
    empty_value_display = '-пусто-'


class PersonalAdmin(admin.ModelAdmin):
    list_display = (
        'tab_number',
        'last_name',
        'first_name',
        'middle_name',
        'position',
        'rank',
        'energy_district',
    )
#     list_editable = ('journal',)
#     search_fields = ('text', 'pub_date')
#     list_filter = ('tab_number',)
    list_display_links = ('first_name', 'last_name', 'middle_name')
    empty_value_display = '-пусто-'


admin.site.register(PostWalking, PostWalkingAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Personal, PersonalAdmin)
admin.site.register(Position)
admin.site.register(EnergyDistrict)
admin.site.register(Brigade, BrigadeAdmin)

admin.site.site_header = '"Кабинет мастера" | Администрирование'
