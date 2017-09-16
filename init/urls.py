from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import home.views

urlpatterns = [
    url(r'^$', home.views.index, name='index'),
    url(r'^db', home.views.db, name='db'),
    url(r'^query', home.views.query, name='query'),
    url(r'^getcrowdedness', home.views.getcrowdedness, name='getcrowdedness'),
    url(r'^updateWifi', home.views.updateWifi, name='updateWifi'),
    url(r'^updateNoise', home.views.updateNoise, name='updateNoise'),
    url(r'^dashboard', home.views.dashboard, name='Dashboard'),
    url(r'^deletealldata', home.views.deletealldata, name='deleteAllData'),
    url(r'^deletecrowdedness', home.views.deletecrowdedness, name='deletecrowdedness'),
    url(r'^admin/', include(admin.site.urls)),
]
