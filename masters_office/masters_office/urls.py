from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


handler404 = 'core.views.page_not_found'
handler403 = 'core.views.csrf_failure'

urlpatterns = [
    path('', include('office.urls', namespace='office')),
    path('admin-mo/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
    # path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
