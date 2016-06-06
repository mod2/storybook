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

    return render_to_response('home.html', {'stories': stories,
                                            'request': request })

@login_required
def story(request, story_slug, scene_id=None, revision_id=None):
    story_obj = Story.objects.get(slug=story_slug)

    scenes = story_obj.scenes.filter(status='active').order_by('order')

    if scene_id is not None:
        selected_scene = story_obj.scenes.filter(id=scene_id).first()
    else:
        selected_scene = scenes.first()

    revision = None
    if selected_scene is not None:
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
                                             'request': request,
                                            })

@login_required
def full_draft(request, story_slug):
    story_obj = Story.objects.get(slug=story_slug)
    scenes = story_obj.scenes.filter(status='active').order_by('order')

    return render_to_response('full_draft.html', {
                                             'story': story_obj,
                                             'scenes': scenes,
                                             'request': request,
                                            })

def ws_reorder_scenes(request, story_slug):
    """ Reorder scenes in a story (called by AJAX) """

    if request.is_ajax() and request.method == 'POST':
        order = json.loads(request.body.decode())['order']

        scenes = Scene.objects.filter(pk__in=order.keys())
        for scene in scenes:
            scene.order = order[unicode(scene.pk)]
            scene.save()

        return JsonResponse(json.dumps({ "status": "success" }), safe=False)

def ws_add_revision(request, story_slug, scene_id):
    """ Add revision to a scene """

    if request.is_ajax() and request.method == 'POST':
        text = json.loads(request.body.decode())['text']

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
        text = json.loads(request.body.decode())['text']

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
        data = json.loads(request.body.decode())
        title = data['title'].strip()
        synopsis = data['synopsis'].strip()

        # Get the scene
        scene = Scene.objects.get(id=scene_id)

        # Update title/synopsis
        scene.title = title
        scene.synopsis = synopsis
        scene.save()

        return JsonResponse(json.dumps({ "status": "success" }), safe=False)
    elif request.is_ajax() and request.method == 'DELETE':
        # Get the scene
        scene = Scene.objects.get(id=scene_id)

        # Remove it
        scene.status = "deleted"
        scene.save()

        return JsonResponse(json.dumps({ "status": "success" }), safe=False)

def ws_add_scene(request, story_slug):
    """ Add a new scene """

    if request.is_ajax() and request.method == 'POST':
        # Get the story
        story = Story.objects.get(slug=story_slug)

        # Get the scene
        scene = Scene()
        scene.story = story
        scene.title = "Untitled"
        scene.synopsis = ""
        scene.order = len(story.scenes.filter(status='active')) + 1
        scene.save()

        return JsonResponse(json.dumps({ "status": "success", "id": scene.id }), safe=False)


def ws_add_story(request):
    """ Add a new story. """

    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body.decode())
        title = data['title'].strip()
        title = title if title else 'Untitled'
        story = Story.objects.create(title=title)
        return JsonResponse(json.dumps({'status': 'success', 'id': story.id}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error', 'error': "Couldn't create a new story."}), safe=False)
