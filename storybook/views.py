# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from .models import Story, Scene, Inbox
from .utils import get_full_draft, make_html

@login_required
def home(request):
    stories = Story.objects.filter(status='active')
    inactive_stories = Story.objects.filter(status='inactive')

    return render_to_response('home.html', {'stories': stories,
                                            'key': settings.SECRET_KEY,
                                            'inactive_stories': inactive_stories,
                                            'request': request })


@login_required
def story(request, story_slug):
    # Get story
    s = Story.objects.get(slug=story_slug)

    scenes = s.scenes.order_by('order')

    return render_to_response('story.html', {'title': s.title,
                                             'story': s,
                                             'key': settings.SECRET_KEY,
                                             'drafts': s.drafts.all(),
                                             'scenes': scenes,
                                             'request': request,
                                            })


@login_required
def story_full(request, story_slug):
    # Get story and scenes
    s = Story.objects.get(slug=story_slug)
    scenes = s.scenes.all().order_by('order')

    return render_to_response('full_draft.html', {
                              'title': "Full Draft — {}".format(s.title),
                              'key': settings.SECRET_KEY,
                              'story': s,
                              'scenes': scenes,
                              'request': request,
                             })


@login_required
def story_organize(request, story_slug):
    # Get story and scenes
    s = Story.objects.get(slug=story_slug)
    scenes = s.scenes.all().order_by('order')

    return render_to_response('organize.html', {
                              'title': "Organize — {}".format(s.title),
                              'story': s,
                              'key': settings.SECRET_KEY,
                              'scenes': scenes,
                              'request': request,
                             })


@login_required
def scene(request, story_slug, scene_id):
    # Get story
    s = Story.objects.get(slug=story_slug)

    # Get scene
    scene = Scene.objects.get(id=scene_id, story__slug=story_slug)

    nav = {}
    nav['next'] = scene.get_next()
    nav['prev'] = scene.get_prev()

    return render_to_response('scene.html', {'title': 'Scene {} — {}'.format(scene.order, s.title),
                                             'scene': scene,
                                             'story': s,
                                             'key': settings.SECRET_KEY,
                                             'nav': nav,
                                             'request': request,
                                            })


@login_required
def scene_edit(request, story_slug, scene_id):
    # Get story
    s = Story.objects.get(slug=story_slug)

    # Get scene
    scene = Scene.objects.get(id=scene_id, story__slug=story_slug)

    return render_to_response('scene_edit.html', {'title': 'Edit Scene {} — {}'.format(scene.order, s.title),
                                             'scene': scene,
                                             'key': settings.SECRET_KEY,
                                             'story': s,
                                             'request': request,
                                            })


@login_required
def story_edit(request, story_slug):
    # Get story
    s = Story.objects.get(slug=story_slug)

    # Get the text
    story_text = get_full_draft(s)

    return render_to_response('story_edit.html', {'title': 'Edit Story — {}'.format(s.title),
                                                  'key': settings.SECRET_KEY,
                                                  'story': s,
                                                  'text': story_text,
                                                  'request': request,
                                                 })


@login_required
def inbox(request):
    # Get inbox
    inbox = Inbox.objects.get(id=1)

    # Get truncated HTML
    excerpt = inbox.get_excerpt()
    html = make_html(excerpt)

    context = {
        'title': 'Inbox',
        'inbox_html': html,
        'key': settings.SECRET_KEY,
        'request': request,
    }

    return render_to_response('inbox.html', context)


@login_required
def inbox_full(request):
    # Get inbox
    inbox = Inbox.objects.get(id=1)

    context = {
        'title': 'Inbox',
        'inbox_html': inbox.html,
        'key': settings.SECRET_KEY,
        'request': request,
    }

    return render_to_response('inbox.html', context)
