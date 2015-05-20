from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', 'django.contrib.auth.views.login', { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', { 'template_name': 'logout.html', 'next_page': '/login/' }, name='logout'),

    url(r'^story/(.+?)/full/$', 'storybook.views.full_draft', name='full_draft'),
    url(r'^story/(.+?)/(.+?)/revision/(.+?)/$', 'storybook.views.story', name='story'),
    url(r'^story/(.+?)/(.+?)/$', 'storybook.views.story', name='story'),
    url(r'^story/(.+?)/$', 'storybook.views.story', name='story'),

    # Web services
    url(r'^api/story/$', 'storybook.views.ws_add_story', name='ws_add_story'),
    url(r'^api/story/(.+?)/reorder-scenes/$', 'storybook.views.ws_reorder_scenes', name='ws_reorder_scenes'),
    url(r'^api/story/(.+?)/(.+?)/add-revision/$', 'storybook.views.ws_add_revision', name='ws_add_revision'),
    url(r'^api/story/(.+?)/(.+?)/update-revision/(.+?)/$', 'storybook.views.ws_update_revision', name='ws_update_revision'),
    url(r'^api/story/(.+?)/add-scene/$', 'storybook.views.ws_add_scene', name='ws_add_scene'),
    url(r'^api/story/(.+?)/(.+?)/$', 'storybook.views.ws_update_scene', name='ws_update_scene'),

    url(r'^$', 'storybook.views.home', name='home'),
)
