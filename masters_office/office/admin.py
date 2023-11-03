from django.contrib import admin
from django.contrib import messages

from .forms import PostWalkingForm, PostRepairWorkForm
from .models import (PostWalking,
                     Personal, District, Position,
                     EnergyDistrict, Brigade, Resolution, PostRepairWork)


admin.site.site_header = '"Кабинет мастера" | Администрирование'
admin.site.index_title = 'Управление кабинетом'

admin.site.register(EnergyDistrict)


class ResolutionInline(admin.TabularInline):
    model = Resolution

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 1
        return max_num


@admin.register(PostRepairWork)
class PostRepairWorkAdmin(admin.ModelAdmin):
    form = PostRepairWorkForm
    list_display = (
        'id',
        'number_post',
        'district',
        'order',
        'number_order',
        'text_for_display',
        'date_start_working',
        'date_end_working',
        'author',
        'is_deleted',
    )
    fields = (
        'district',
        'order',
        'number_order',
        'description',
        'date_start_working',
        'date_end_working',
        'author',
        'is_deleted',
    )
    list_display_links = ('number_post', 'text_for_display')
    search_fields = ('description', 'date_start_working', 'date_end_working')
    list_filter = ('district', 'date_start_working', 'date_end_working', 'is_deleted', 'author')
    empty_value_display = '-пусто-'
    list_per_page = 20
    save_on_top = True
    readonly_fields = ('time_create', 'time_update', 'number_post')


@admin.register(PostWalking)
class PostWalkingAdmin(admin.ModelAdmin):
    form = PostWalkingForm
    inlines = (ResolutionInline,)
    list_display = (
        'id',
        'number_post',
        'district',
        'planned',
        'not_planned',
        'walk_date',
        'task',
        'text_for_display',
        'author',
        'is_deleted',
    )
    fields = (
        'author',
        'district',
        ('time_create', 'time_update'),
        ('planned', 'not_planned'),
        'walk_date',
        'members',
        'task',
        'text',
        'plan',
        'fix_date',
        'transfer',
        'is_deleted',
    )
    list_display_links = ('number_post', 'task')
    search_fields = ('text', 'walk_date')
    list_filter = ('walk_date', 'is_deleted',)
    empty_value_display = '-пусто-'
    save_on_top = True
    readonly_fields = ('time_create', 'time_update', 'number_post')
    filter_horizontal = ('members',)
    list_per_page = 20


@admin.register(Brigade)
class BrigadeAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'master',
        'brigadier',
    )
    list_display_links = (
        'number',
        'master',
    )
    filter_horizontal = ('members',)
    empty_value_display = '-пусто-'


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'master',
        'energy_district',
        'slug',
    )
    list_editable = ('master', 'energy_district')
    list_display_links = ('title',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Personal)
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
    list_display_links = ('first_name', 'last_name', 'middle_name')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'name_position',
        'walker',
    )
    list_editable = ('walker',)
    list_display_links = ('name_position',)
    empty_value_display = '-пусто-'


@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'id',
        'author',
        'post_walking',
        'text',
    )
    list_display_links = ('author', 'post_walking', 'text')
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        if PostWalking.objects.get(id=request.POST['post_walking']).resolution.all() and not change:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'Резолюция не добавлена, у записи уже есть резолюция!'
            )
        super().save_model(request, obj, form, change)
