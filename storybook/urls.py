from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from storybook import views as sb_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', auth_views.login, { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/', auth_views.logout, { 'template_name': 'logout.html', 'next_page': '/login/' }, name='logout'),

    # Scenes/revisions
    url(r'^story/(.+?)/(.+?)/revision/(.+?)/$', sb_views.scene, name='scene'),
    url(r'^story/(.+?)/(.+?)/$', sb_views.scene, name='scene'),

    # Story
    url(r'^story/(.+?)/full/$', sb_views.full_draft, name='full_draft'),
    url(r'^story/(.+?)/$', sb_views.story, name='story'),

    # Web services
    url(r'^api/story/$', sb_views.ws_add_story, name='ws_add_story'),
    url(r'^api/story/(.+?)/reorder-scenes/$', sb_views.ws_reorder_scenes, name='ws_reorder_scenes'),
    url(r'^api/story/(.+?)/(.+?)/add-revision/$', sb_views.ws_add_revision, name='ws_add_revision'),
    url(r'^api/story/(.+?)/(.+?)/update-revision/(.+?)/$', sb_views.ws_update_revision, name='ws_update_revision'),
    url(r'^api/story/(.+?)/add-scene/$', sb_views.ws_add_scene, name='ws_add_scene'),
    url(r'^api/story/(.+?)/(.+?)/$', sb_views.ws_update_scene, name='ws_update_scene'),

    url(r'^$', sb_views.home, name='home'),
]
