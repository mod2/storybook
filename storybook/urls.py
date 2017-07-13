from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from storybook import apis as sb_apis
from storybook import views as sb_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', auth_views.login, { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/', auth_views.logout, { 'template_name': 'logout.html', 'next_page': '/login/' }, name='logout'),

    url(r'^inbox/full/$', sb_views.inbox_full, name='inbox_full'),
    url(r'^inbox/$', sb_views.inbox, name='inbox'),

    # Story
    url(r'^story/(?P<story_slug>[^\/]+)/full/$', sb_views.story_full, name='story_full'),
    url(r'^story/(?P<story_slug>[^\/]+)/organize/$', sb_views.story_organize, name='story_organize'),
    url(r'^story/(?P<story_slug>[^\/]+)/edit/$', sb_views.story_edit, name='story_edit'),
    url(r'^story/(?P<story_slug>[^\/]+)/$', sb_views.story, name='story'),

    # Scenes
    url(r'^story/(?P<story_slug>[^\/]+)/(?P<scene_id>[^\/]+)/edit/$', sb_views.scene_edit, name='scene_edit'),
    url(r'^story/(?P<story_slug>[^\/]+)/(?P<scene_id>[^\/]+)/$', sb_views.scene, name='scene'),

    # Web services
    url(r'^api/payload/$', sb_apis.api_process_payload, name='api_process_payload'),
    url(r'^api/story/(?P<story_slug>[^\/]+)/reorder-scenes/$', sb_apis.api_reorder_scenes, name='api_reorder_scenes'),
    url(r'^api/story/(?P<story_slug>[^\/]+)/save-story/$', sb_apis.api_save_story, name='api_save_story'),
    url(r'^api/story/(?P<story_slug>[^\/]+)/save-draft/$', sb_apis.api_save_draft, name='api_save_draft'),
    url(r'^api/story/(?P<story_slug>[^\/]+)/get-draft/$', sb_apis.api_get_draft, name='api_get_draft'),
    url(r'^api/story/(?P<story_slug>[^\/]+)/(?P<scene_id>[^\/]+)/$', sb_apis.api_save_scene, name='api_save_scene'),

    # Home
    url(r'^$', sb_views.home, name='home'),
]
