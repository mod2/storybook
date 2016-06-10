# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
import json

from .models import Story, Scene, Revision

@login_required
def home(request):
    stories = Story.objects.filter(status='active')
    inactive_stories = Story.objects.filter(status='inactive')

    return render_to_response('home.html', {'stories': stories,
                                            'inactive_stories': inactive_stories,
                                            'request': request })

@login_required
def story(request, story_slug):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story
    s = Story.objects.get(slug=story_slug)

    scenes = s.scenes.exclude(status='discarded').order_by('order')

    return render_to_response('story.html', {'title': s.title,
                                             'story': s,
                                             'scenes': scenes,
                                             'stories': stories,
                                             'request': request,
                                            })

@login_required
def scene(request, story_slug, scene_id, revision_id=None):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story
    s = Story.objects.get(slug=story_slug)

    # Get scene
    scene = Scene.objects.get(id=scene_id, story__slug=story_slug)

    return render_to_response('scene.html', {'title': 'Scene {} — {}'.format(scene.order, s.title),
                                             'scene': scene,
                                             'story': s,
                                             'stories': stories,
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
                                             'story': s,
                                             'stories': stories,
                                             'request': request,
                                            })

@login_required
def story_full(request, story_slug):
    # Boilerplate
    stories = Story.objects.filter(status='active')

    # Get story and scenes
    s = Story.objects.get(slug=story_slug)
    scenes = s.active_scenes().order_by('order')

    return render_to_response('full_draft.html', {
                              'story': s,
                              'scenes': scenes,
                              'stories': stories,
                              'request': request,
                             })


