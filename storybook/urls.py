from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'storybook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^story/(.+?)/(.+?)/revision/(.+?)/$', 'storybook.views.story', name='story'),
    url(r'^story/(.+?)/(.+?)/$', 'storybook.views.story', name='story'),
    url(r'^story/(.+?)/$', 'storybook.views.story', name='story'),

    # Web services
    url(r'^api/story/(.+?)/reorder-scenes/$', 'storybook.views.ws_reorder_scenes', name='ws_reorder_scenes'),
    url(r'^api/story/(.+?)/(.+?)/add-revision/$', 'storybook.views.ws_add_revision', name='ws_add_revision'),
    url(r'^api/story/(.+?)/(.+?)/update-revision/(.+?)/$', 'storybook.views.ws_update_revision', name='ws_update_revision'),
    url(r'^api/story/(.+?)/add-scene/$', 'storybook.views.ws_add_scene', name='ws_add_scene'),
    url(r'^api/story/(.+?)/(.+?)/$', 'storybook.views.ws_update_scene', name='ws_update_scene'),

    url(r'^$', 'storybook.views.home', name='home'),
)
