from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'storybook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^story/(.+?)/$', 'storybook.views.story', name='story'),
    url(r'^$', 'storybook.views.home', name='home'),
)
