# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
import json

from .models import Story, Scene

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
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story
    s = Story.objects.get(slug=story_slug)

    scenes = s.scenes.order_by('order')

    return render_to_response('story.html', {'title': s.title,
                                             'story': s,
                                             'key': settings.SECRET_KEY,
                                             'fragments': s.fragments.all(),
                                             'drafts': s.drafts.all(),
                                             'scenes': scenes,
                                             'stories': stories,
                                             'request': request,
                                            })

@login_required
def story_full(request, story_slug):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story and scenes
    s = Story.objects.get(slug=story_slug)
    scenes = s.scenes.all().order_by('order')

    return render_to_response('full_draft.html', {
                              'title': "Full Draft — {}".format(s.title),
                              'key': settings.SECRET_KEY,
                              'story': s,
                              'scenes': scenes,
                              'stories': stories,
                              'request': request,
                             })

@login_required
def story_organize(request, story_slug):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story and scenes
    s = Story.objects.get(slug=story_slug)
    scenes = s.scenes.all().order_by('order')

    return render_to_response('organize.html', {
                              'title': "Organize — {}".format(s.title),
                              'story': s,
                              'key': settings.SECRET_KEY,
                              'scenes': scenes,
                              'stories': stories,
                              'request': request,
                             })

@login_required
def story_fragments(request, story_slug):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story and scenes
    s = Story.objects.get(slug=story_slug)

    return render_to_response('fragments.html', {
                              'title': "Fragments — {}".format(s.title),
                              'story': s,
                              'key': settings.SECRET_KEY,
                              'fragments': s.fragments.all(),
                              'stories': stories,
                              'request': request,
                             })
@login_required
def scene(request, story_slug, scene_id):
    # Boilerplate
    stories = Story.objects.filter(status='active')

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
                                             'stories': stories,
                                             'nav': nav,
                                             'request': request,
                                            })

@login_required
def scene_edit(request, story_slug, scene_id):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story
    s = Story.objects.get(slug=story_slug)

    # Get scene
    scene = Scene.objects.get(id=scene_id, story__slug=story_slug)

    return render_to_response('editscene.html', {'title': 'Edit Scene {} — {}'.format(scene.order, s.title),
                                             'scene': scene,
                                             'key': settings.SECRET_KEY,
                                             'story': s,
                                             'stories': stories,
                                             'request': request,
                                            })

