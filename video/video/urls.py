from django.conf.urls.static import static
from django.urls import path, include

# from video.video import settings

urlpatterns = [
    path('', include('VideoApp.urls'))
]

# if settings.DEBAG:
#     urlpatterns += static(settings.MEDIA_URL, dociment_root=settings.MEDIA_ROOT)