from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

#mappa il nome museum-home alla view home definita in views che restituisce una http response
urlpatterns = [
    path('', views.home, name='museum-home'),
    path('map/', views.map, name='museum-map'),
    path('about/', views.about, name='museum-about'),
    path('statistics/', views.statistics, name='museum-statistics'),
]


# solo per debug, da cancellare prima del deploy su aws!!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)