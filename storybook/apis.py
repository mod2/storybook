# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
import json

from .models import Story, Scene, Revision
from .utils import process_payload

def api_update_revision(request, story_slug, scene_id, revision_id):
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

def api_update_scene(request, story_slug, scene_id):
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

def api_add_scene(request, story_slug):
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

def api_add_story(request):
    """ Add a new story. """

    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body.decode())
        title = data['title'].strip()
        title = title if title else 'Untitled'
        story = Story.objects.create(title=title)
        return JsonResponse(json.dumps({'status': 'success', 'id': story.id}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error', 'error': "Couldn't create a new story."}), safe=False)


## New

@login_required
def api_process_payload(request):
    """ Processes a payload. """

    if request.method == 'GET':
        payload = request.GET.get('payload', '').strip()
        key = request.GET.get('key', '')
    elif request.method == 'POST':
        payload = request.POST.get('payload', '').strip()
        key = request.POST.get('key', '')

    callback = request.GET.get('callback', '')

    # Make sure we have the secret key
    if key != settings.SECRET_KEY:
        return JsonResponse({})

    # Add the sequence
    status, message = process_payload(payload)

    response = {
        'status': status,
        'message': message,
    }

    if callback:
        # Redirect to callback
        response = HttpResponse("", status=302)
        response['Location'] = callback
        return response
    else:
        # Return JSON response
        return JsonResponse(response)

def api_reorder_scenes(request, story_slug):
    """ Reorder scenes in a story (called by AJAX) """

    if request.method == 'POST':
        key = request.POST.get('key', '')

    # Make sure we have the secret key
    if key != settings.SECRET_KEY:
        return JsonResponse({})

    id_list = [int(x) for x in request.POST.get('ids', '').split(',') if x != '']

    for index, scene_id in enumerate(id_list):
        scene = Scene.objects.get(id=scene_id, story__slug=story_slug)
        scene.order = index + 1
        scene.save()

    return JsonResponse(json.dumps({ "status": "success" }), safe=False)

def api_save_scene(request, story_slug, scene_id):
    """ Add revision to a scene. """

    if request.method == 'POST':
        key = request.POST.get('key', '')

    # Make sure we have the secret key
    if key != settings.SECRET_KEY:
        return JsonResponse({})

    text = request.POST.get('text', '')

    # Get the scene
    scene = Scene.objects.get(id=scene_id)

    # Create the revision
    revision = Revision()
    revision.scene = scene
    revision.text = text.strip()
    revision.save()

    return JsonResponse(json.dumps({ "status": "success", "id": revision.id }), safe=False)
