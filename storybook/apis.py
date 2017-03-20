# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
from django.utils import timezone
import json

from .models import Story, Scene
from .utils import process_payload, make_new_draft

def api_update_scene(request, story_slug, scene_id):
    """
    Update scene metadata.
    """

    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body.decode())
        title = data['title'].strip()

        # Get the scene
        scene = Scene.objects.get(id=scene_id)

        # Update title/synopsis
        scene.title = title
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
    """
    Add a new scene.
    """

    if request.is_ajax() and request.method == 'POST':
        # Get the story
        story = Story.objects.get(slug=story_slug)

        # Get the scene
        scene = Scene()
        scene.story = story
        scene.title = "Untitled"
        scene.order = len(story.scenes.filter(status='active')) + 1
        scene.save()

        return JsonResponse(json.dumps({ "status": "success", "id": scene.id }), safe=False)

def api_add_story(request):
    """
    Add a new story.
    """

    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body.decode())
        title = data['title'].strip()
        title = title if title else 'Untitled'
        story = Story.objects.create(title=title)
        return JsonResponse(json.dumps({'status': 'success', 'id': story.id}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error', 'error': "Couldn't create a new story."}), safe=False)


## New

@csrf_exempt
def api_process_payload(request):
    """
    Processes a payload.
    """

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
    """
    Reorder scenes in a story (called by AJAX).
    """

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

    # Make new draft
    story = Story.objects.get(slug=story_slug)
    make_new_draft(story)

    return JsonResponse({ "status": "success" })

def api_save_scene(request, story_slug, scene_id):
    """
    Add revision to a scene.
    """

    if request.method == 'POST':
        key = request.POST.get('key', '')

    # Make sure we have the secret key
    if key != settings.SECRET_KEY:
        return JsonResponse({})

    text = request.POST.get('text', '')

    # Get the scene
    scene = Scene.objects.get(story__slug=story_slug, id=scene_id)

    if '\n## ' or ':scene' in text:
        # There's a ##, so split on the scene

        # First normalize to ##
        text = text.replace(':scene', '\n##')

        # Split on ##
        data = text.split('\n## ')

        # Save [0] to the scene
        scene.text = data[0].strip()
        scene.save()

        d_len = len(data)
        if d_len > 1:
            # New scene(s), so first reorder following scenes
            for index, scn in enumerate(Scene.objects.filter(story__slug=story_slug, order__gt=scene.order)):
                # Move them d_len forward in the order list
                scn.order = scn.order + d_len - 1
                scn.save()

            # Now go through and make each new scene
            for i, d in enumerate(data[1:]):
                scene_data = data[i+1]

                # strip out title vs. text
                lines = scene_data.split('\n\n')
                scene_title = lines[0].strip()
                scene_text = '\n\n'.join(lines[1:]).strip()

                # create a new scene object
                new_scene = Scene()
                new_scene.title = scene_title
                new_scene.story = scene.story
                new_scene.order = scene.order + i + 1
                new_scene.text = scene_text
                new_scene.save()
    else:
        # No new scenes
        scene.text = text.strip()
        scene.save()

    # Update last_modified on the story
    story = Story.objects.get(slug=story_slug)
    story.last_modified = timezone.now()
    story.save()

    return JsonResponse({ "status": "success"})

def api_save_draft(request, story_slug):
    """
    Saves a new draft of a story.
    """

    try:
        if request.method == 'POST':
            key = request.POST.get('key', '')

        # Make sure we have the secret key
        if key != settings.SECRET_KEY:
            return JsonResponse({})

        # Make new draft and update last_modified
        story = Story.objects.get(slug=story_slug)
        make_new_draft(story)

        return JsonResponse({ "status": "success"})
    except Exception as e:
        return JsonResponse({ "status": "error"}, status_code=500)
