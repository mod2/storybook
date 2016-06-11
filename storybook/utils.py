from django.conf import settings

import json

from .models import Story, Scene, Revision, Fragment, Character


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
            for story in Story.objects.all():
                pass

            story.save()
        except Exception as e:
            print("Couldn't create story", e)
            pass

    return story


def get_or_create_character(name, story, scene):
    character = None

    # Try to get the character
    try:
        character = Character.objects.get(name=name, story=story)

        # Add to this scene
        character.scenes.add(scene)
        character.save()
    except Exception as e:
        pass

    # Not found, so create it
    if character is None:
        try:
            character = Character()
            character.name = name
            character.story = story
            character.save()
            character.color = character.get_random_color()
            character.scenes.add(scene)
            character.save()
        except Exception as e:
            print("Couldn't create character", e)
            pass

    return character


def process_scenes(payload):
    """ Takes a payload and returns a list of scenes. """

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
            # Story title (get everything after ::story)
            response['story'] = ' '.join(line[2:].split(' ')[1:]).strip()
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
            elif keyword == 'synopsis':
                # Add synopsis to current scene
                current_scene['synopsis'] = parameters
            elif keyword == 'characters':
                # Add character list to current scene
                current_scene['characters'] = [x.strip() for x in parameters.split(',')]
        else:
            if current_scene:
                current_scene['fragments'].append(line)
            else:
                response['fragments'].append(line)

    return response


def process_payload(payload):
    """ Takes a payload and parses it out. """
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
        f = Fragment()
        f.story = story
        f.text = '\n'.join(response['fragments']).strip()
        f.save()

    # Now go through any scenes
    for index, scene in enumerate(scenes):
        try:
            # Create scene
            s = Scene()
            s.story = story
            s.title = scene['title']
            if 'synopsis' in scene:
                s.synopsis = scene['synopsis']
            s.order = 500 + index
            s.save()

            if 'characters' in scene:
                for name in scene['characters']:
                    c = get_or_create_character(name, story, s)

            # Create the revision
            r = Revision()
            r.text = '\n'.join(scene['fragments']).strip()
            r.scene = s
            r.save()
        except Exception as e:
            status = 'error'
            message = e

    # Finally, reorder the scenes
    for index, scene in enumerate(story.scenes.all()):
        scene.order = index + 1
        scene.save()

    return status, message


