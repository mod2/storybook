from django.core.management.base import BaseCommand, CommandError

from storybook.models import Scene

class Command(BaseCommand):
    args = '<json file>'
    help = 'Generates HTML for every scene'

    def handle(self, *args, **options):
        try:
            scenes = Scene.objects.all()

            for scene in scenes:
                if scene.text and scene.text != '':
                    scene.html = scene.make_html(scene.text)
                    scene.save()
        except Exception as e:
            print(e)
