from django.conf import settings

import datetime
import json
import mistune
import re
import smartypants

from .models import Story, Scene, Draft, Inbox, InboxEntry


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
                # Slug, need to turn it into a title
                story.title = story_slug.replace("-", " ").title()
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
    }
    current_scene = None

    if payload == '':
        return {}

    for line in payload.split('\n'):
        line = line.strip()

        if len(line) >= 1 and line[0:2] == '::':
            # Story slug (get everything after :: up to the next space)
            # and ignore everything after that
            response['story'] = line[2:].split(' ')[0].strip()
        elif len(line) >= 1 and line[0] == ':':
            # Metadata 
            bits = line[1:].split(' ')
            keyword = bits[0]
            parameters = ' '.join(bits[1:])
        elif len(line) >= 3 and line[0:2] == '##':
            # New scene (title)
            response['scenes'].append({
                'title': line[2:].strip(),
                'lines': [],
            })
            current_scene = response['scenes'][-1]
        else:
            if not current_scene:
                # Create a new untitled scene
                response['scenes'].append({
                    'title': 'Untitled Scene',
                    'lines': [],
                })
                current_scene = response['scenes'][-1]

            # Add the line to the current scene
            current_scene['lines'].append(line)

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

        # Now go through any scenes
        for index, scene in enumerate(scenes):
            try:
                # Create scene
                s = Scene()
                s.story = story
                s.title = scene['title']
                s.order = 500 + index
                s.text = '\n'.join(scene['lines']).strip()
                s.html = make_html(s.text)
                s.word_count = word_count(s.text)
                s.save()
            except Exception as e:
                status = 'error'
                message = e

        # Finally, reorder the scenes
        for index, scene in enumerate(story.scenes.all()):
            scene.order = index + 1
            scene.save()
    else:
        # No story, we're in inbox mode
        text = ''
        for scene in scenes:
            if scene['title'] != 'Untitled Scene':
                text += '## {}\n\n'.format(scene['title'])
            text += '\n'.join(scene['lines']).strip()
            text += '\n\n'
        text = text.strip()

        # Get or create inbox
        try:
            inbox = Inbox.objects.get(id=1)
            inbox.text += '\n\n{}'.format(text)
        except:
            inbox = Inbox()
            inbox.text = text

        inbox.save()

        # Create a new entry
        entry = InboxEntry()
        entry.text = text
        entry.inbox = inbox
        entry.save()

    return status, message


def get_full_draft(story):
    """
    Gets a full plain-text draft of the given story.
    """
    scenes = story.scenes.all().order_by('order')

    # Story title
    response = '::{} -- v{} -- {}\n'.format(story.slug, str(story.drafts.count()).zfill(3), datetime.date.today().strftime("%Y-%m-%d"))

    for scene in scenes:
        if scene.title or scene.text:
            if scene.title:
                response += '\n## {}\n'.format(scene.title)
            else:
                response += '\n## Untitled Scene\n'

            response += '\n'

            if scene.text is not None:
                response += '{}\n\n'.format(scene.text)#.encode('utf-8'))

    return response.strip()


def make_new_draft(story):
    """
    Makes a new draft for a given story.
    """
    draft = Draft()
    draft.story = story
    draft.story_text = get_full_draft(story)
    draft.save()


def make_html(text):
    """
    Renders a string to HTML.
    """
    # Treat horizontal rules kindly
    html = text.replace('---', '%%%HR%%%')

    html = mistune.markdown(smartypants.smartypants(html))

    # Wrap comments
    html = re.sub(r"<p>\/\/(.+?)<\/p>", r"<div class='comment'>\1</div>", html)

    html = html.replace('<p>%%%HR%%%</p>', '<hr/>')

    return html


def word_count(text):
    """
    Returns word count for a string.
    """
    if text is None or text == '':
        return 0

    # Get rid of extra space
    t = text.strip()

    # Remove comments
    t = re.sub(r"\/\/(.+?)(\n|$)", "", t)

    # Remove newlines
    t = t.replace("\n", " ").replace("  ", " ").strip()

    # Split by spaces
    words = re.split(r"\s+", t)

    if len(words) == 1 and words[0] == '':
        return 0
    else:
        return len(words)
