# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
import json

from .models import Story, Scene, Revision

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

def ws_reorder_scenes(request, story_slug):
    """ Reorder scenes in a story (called by AJAX) """

    if request.is_ajax() and request.method == 'POST':
        order = json.loads(request.body)['order']

        scenes = Scene.objects.filter(pk__in=order.keys())
        for scene in scenes:
            scene.order = order[unicode(scene.pk)]
            scene.save()

        return JsonResponse(json.dumps({ "status": "success" }), safe=False)

def ws_add_revision(request, story_slug, scene_id):
    """ Add revision to a scene """

    if request.is_ajax() and request.method == 'POST':
        text = json.loads(request.body)['text']

        if text.strip() == '':
            return ''

        # Get the scene
        scene = Scene.objects.get(id=scene_id)

        # Create the revision
        revision = Revision()
        revision.scene = scene
        revision.text = text.strip()
        revision.save()

        return JsonResponse(json.dumps({ "status": "success", "id": revision.id }), safe=False)

def ws_update_revision(request, story_slug, scene_id, revision_id):
    """ Update revision for a scene """

    if request.is_ajax() and request.method == 'POST':
        text = json.loads(request.body)['text']

        if text.strip() == '':
            return ''

        # Get the scene
        scene = Scene.objects.get(id=scene_id)

        # Get the revision
        revision = Revision.objects.get(id=revision_id)

        # Update the revision
        revision.text = text.strip()
        revision.save()

        return JsonResponse(json.dumps({ "status": "success", "id": revision.id }), safe=False)

def ws_update_scene(request, story_slug, scene_id):
    """ Update scene metadata """

    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body)
        title = data['title'].strip()
        synopsis = data['synopsis'].strip()

        # Get the scene
        scene = Scene.objects.get(id=scene_id)

        # Update title/synopsis
        scene.title = title
        scene.synopsis = synopsis
        scene.save()

        return JsonResponse(json.dumps({ "status": "success" }), safe=False)
