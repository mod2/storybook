from django.conf import settings

import datetime
import json

from .models import Story, Scene, Fragment, Draft


def get_or_create_story(story_slug):
    story = None

    # Try to get the story
    try:
        story = Story.objects.get(slug=story_slug)
    except Exception as e:
        try:
            story = Story.objects.get(title__icontains=story_slug)
        except Exception as e:
            pass

    # Not found, so create it
    if story is None:
        try:
            story = Story()

            if story_slug[0].islower():
                # Slug, need to capitalize it
                story.title = story_slug.capitalize()
            else:
                # Title
                story.title = story_slug

            story.order = 0 # put at beginning

            # Reorder the other stories
            for s in Story.objects.all():
                s.order = s.order + 1

            story.save()
        except Exception as e:
            print("Couldn't create story", e)

    return story


def process_scenes(payload):
    """
    Takes a payload and returns a list of scenes.
    """

    response = {
        'scenes': [],
        'fragments': [],
    }
    current_fragment = []
    current_scene = None

    if payload == '':
        return {}

    for line in payload.split('\n'):
        line = line.strip()

        if len(line) >= 1 and line[0:2] == '::':
            # Story slug (get everything after ::)
            response['story'] = line[2:].strip()
        elif len(line) >= 3 and line[0:2] == '##':
            # New scene
            response['scenes'].append({
                'title': line[2:].strip(),
                'fragments': [],
            })
            current_scene = response['scenes'][-1]
        elif len(line) >= 1 and line[0] == ':':
            # Metadata 
            bits = line[1:].split(' ')
            keyword = bits[0]
            parameters = ' '.join(bits[1:])

            if keyword == 'scene':
                # New scene
                response['scenes'].append({
                    'title': parameters,
                    'fragments': [],
                })
                current_scene = response['scenes'][-1]
        elif line.strip() != '':
            if current_scene:
                current_scene['fragments'].append(line)
            else:
                response['fragments'].append(line)

    return response


def process_payload(payload):
    """
    Takes a payload and parses it out.
    """
    status = 'success'
    message = ''

    response = process_scenes(payload)

    if len(response) == 0:
        status = 'error'
        message = "Empty payload"
        scenes = []
    else:
        scenes = response['scenes']

    # Get the story first
    if 'story' in response:
        story = get_or_create_story(response['story'])
    else:
        story = get_or_create_story('Untitled')
    
    # If we haven't specified a scene, we've just got a fragment
    if 'fragments' in response:
        f_text = '\n'.join(response['fragments']).strip()
        if f_text != '':
            f = Fragment()
            f.story = story
            f.text = f_text
            f.save()

    # Now go through any scenes
    for index, scene in enumerate(scenes):
        try:
            # Create scene
            s = Scene()
            s.story = story
            s.title = scene['title']
            s.order = 500 + index
            s.text = '\n'.join(scene['fragments']).strip()
            s.save()
        except Exception as e:
            status = 'error'
            message = e

    # Finally, reorder the scenes
    for index, scene in enumerate(story.scenes.all()):
        scene.order = index + 1
        scene.save()

    return status, message


def get_full_draft(story):
    """
    Gets a full plain-text draft of the given story.
    """
    scenes = story.scenes.all().order_by('order')

    # Story title
    response = '# {} -- v{} -- {}\n'.format(story.title, str(story.drafts.count()).zfill(3), datetime.date.today().strftime("%Y-%m-%d"))

    for scene in scenes:
        if scene.title or scene.text:
            if scene.title:
                response += '\n## {}\n'.format(scene.title)
            else:
                response += '\n## Untitled Scene\n'

            response += '\n'

            if scene.text is not None:
                response += '{}\n\n'.format(scene.text)

    return response.strip()


def make_new_draft(story):
    """
    Makes a new draft for a given story.
    """
    draft = Draft()
    draft.story = story
    draft.story_text = get_full_draft(story)
    draft.save()
