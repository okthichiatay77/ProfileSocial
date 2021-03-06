from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.conf import settings

urlpatterns = [
    path('', include('posts.urls')),
    path('acc/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
