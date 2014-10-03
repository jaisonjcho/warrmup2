from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'logincounter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'logincounter.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/login', 'logincounter.views.login', name='login'),
    url(r'^users/add', 'logincounter.views.add', name='add'),
    url(r'^TESTAPI/resetFixture', 'logincounter.views.resetFixture', name='resetFixture'),
    url(r'^TESTAPI/unitTests', 'logincounter.views.unitTests', name='unitTests'),
)