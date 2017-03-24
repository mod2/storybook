from django.core.management.base import BaseCommand, CommandError

from storybook.models import Scene
from storybook.utils import make_html, word_count

class Command(BaseCommand):
    args = '<json file>'
    help = 'Generates HTML for every scene'

    def handle(self, *args, **options):
        try:
            scenes = Scene.objects.all()

            for scene in scenes:
                if scene.text and scene.text != '':
                    scene.html = make_html(scene.text)
                    scene.word_count = word_count(scene.text)
                    scene.save()
        except Exception as e:
            print(e)
