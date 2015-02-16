# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
import json

from .models import Story, Scene

#@login_required
def home(request):
    return render_to_response('home.html', { })

#@login_required
def story(request, story_slug, scene_id=None, revision_id=None):
    story_obj = Story.objects.get(slug=story_slug)

    scenes = story_obj.scenes.filter(status='active').order_by('order')

    if scene_id is not None:
        selected_scene = story_obj.scenes.filter(id=scene_id).first()
    else:
        selected_scene = scenes.first()

    # Get the appropriate revision
    if revision_id is not None:
        revision = selected_scene.revisions.filter(id=revision_id).first()
    else:
        revision = selected_scene.latest_revision()

    return render_to_response('story.html', {'pagetitle': story_obj.title,
                                             'story': story_obj,
                                             'scenes': scenes,
                                             'selected_scene': selected_scene,
                                             'revision': revision,
                                            })
