from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('', RedirectView.as_view(url=' main/', permanent=True))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)