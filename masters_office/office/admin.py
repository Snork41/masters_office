from django.contrib import admin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import PostWalkingForm, PostRepairWorkForm, PostOrderForm
from .models import (PostWalking,
                     Personal, District, Position,
                     EnergyDistrict, Brigade, Resolution, PostRepairWork, PostOrder, StaticBlock)


admin.site.site_header = '"Кабинет мастера" | Администрирование'
admin.site.index_title = 'Управление кабинетом'


@admin.register(StaticBlock)
class StaticBlockAdmin(admin.ModelAdmin):
    pass


class HasResolutionFilter(admin.SimpleListFilter):
    """Фильтр записей обходов по наличию резолюции."""

    title = 'Есть резолюция'
    parameter_name = 'has_resolution'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(resolution__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(resolution__isnull=True)


@admin.register(EnergyDistrict)
class EnergyDistrictAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )


@admin.register(PostOrder)
class PostOrderAdmin(admin.ModelAdmin):
    form = PostOrderForm
    list_display = (
        'number_post',
        'district',
        'order',
        'number_order',
        'description',
        'foreman',
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
        'foreman',
        'members',
        'author',
        ('date_start_working', 'date_end_working'),
        'is_deleted',
    )
    list_editable = ('is_deleted',)
    list_display_links = ('number_post', 'order', 'number_order', 'description')
    list_filter = ('order', 'district', 'date_start_working', 'date_end_working', 'is_deleted', 'author')
    empty_value_display = '-пусто-'
    list_per_page = 20
    save_on_top = True
    readonly_fields = ('time_create', 'time_update')


@admin.register(PostRepairWork)
class PostRepairWorkAdmin(admin.ModelAdmin):
    form = PostRepairWorkForm
    list_display = (
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
        ('date_start_working', 'date_end_working'),
        'author',
        'is_deleted',
    )
    list_editable = ('is_deleted',)
    list_display_links = ('number_post', 'text_for_display')
    search_fields = ('description', 'date_start_working', 'date_end_working')
    list_filter = ('district', 'date_start_working', 'date_end_working', 'is_deleted', 'author')
    empty_value_display = '-пусто-'
    list_per_page = 20
    save_on_top = True
    readonly_fields = ('time_create', 'time_update', 'number_post')


class ResolutionInline(admin.TabularInline):
    """Отображение резолюции при создании/изменении записи обхода."""

    model = Resolution

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 1
        return max_num


@admin.register(PostWalking)
class PostWalkingAdmin(admin.ModelAdmin):
    form = PostWalkingForm
    inlines = (ResolutionInline,)
    list_display = (
        'number_post',
        'district',
        'planned',
        'not_planned',
        'walk_date',
        'task',
        'text_for_display',
        'author',
        'has_resolution',
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
    list_editable = ('is_deleted',)
    list_display_links = ('number_post', 'task')
    search_fields = ('text', 'walk_date')
    list_filter = ('walk_date', 'is_deleted', 'district', HasResolutionFilter)
    empty_value_display = '-пусто-'
    save_on_top = True
    readonly_fields = ('time_create', 'time_update', 'number_post')
    filter_horizontal = ('members',)
    list_per_page = 20

    @admin.display(description='Замечания, выявленные при обходе')
    def text_for_display(self, post):
        if len(post.text) > 15:
            return f'{post.text[:20]}...'
        return post.text

    @admin.display(description='Есть резолюция', boolean=True)
    def has_resolution(self, post):
        return post.resolution.exists()


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
        'foreman',
    )
    list_display_links = ('first_name', 'last_name', 'middle_name')
    list_filter = ('energy_district', 'position')
    list_editable = ('foreman',)


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
        'id',
        'author',
        'post_walking',
        'district',
        'text',
        'viewed'
    )
    list_display_links = ('author', 'post_walking', 'text')
    empty_value_display = '-пусто-'
    actions = ('view_resolution', 'unread_resolution')

    @admin.display(description='Источник (район)')
    def district(self, resolution):
        return resolution.post_walking.district

    @admin.action(description='Отметить резолюцию прочитанной')
    def view_resolution(self, request, queryset):
        count = queryset.update(viewed=True)
        self.message_user(request, f'Количество прочитанных резолюций: {count}')

    @admin.action(description='Отметить резолюцию непрочитанной')
    def unread_resolution(self, request, queryset):
        count = queryset.update(viewed=False)
        self.message_user(request, f'Количество непрочитанных резолюций: {count}')

    def save_model(self, request, obj, form, change):
        if get_object_or_404(PostWalking, id=request.POST.get('post_walking')).resolution.all() and not change:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 'Резолюция не добавлена, у записи уже есть резолюция!'
            )
        super().save_model(request, obj, form, change)
