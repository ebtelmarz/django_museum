"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('museum/', include('museum.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# mapping degli url alle pagine che creo
# quando scrivo /museum nella barra del browser lui cerca un match con quella stringa in
# questa lista, e vede cosa deve fare, include cancella da ciò che ha come argomento tutto
# ciò che è già stato matchato come museum, ovvero 'museum.urls' e guarda il resto,
# quindi in questo caso la stringa vuota, e questa la manda a museum.urls dove
# cerca ciò che è rimasto quindi la stringa vuota il cui mapping deve ritornarmi
# ciò che ho definito nella funzione views.home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('museum.urls')),
]



























