from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField

import mistune
import re
import smartypants


class Story(models.Model):
    STATUSES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('abandoned', 'Abandoned'),
        ('finished', 'Finished'),
    )

    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES,
                              default=STATUSES[0][0])
    created = models.DateTimeField(default=timezone.now())
    last_modified = models.DateTimeField(default=timezone.now())
    order = models.PositiveSmallIntegerField(default=50)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def active_scenes(self):
        return self.scenes.exclude(status='discarded')

    def word_count(self):
        word_count = 0

        for scene in self.active_scenes():
            word_count += scene.word_count()

        return word_count

    def description_rendered(self):
        return smartypants.smartypants(self.description)

    class Meta:
        verbose_name_plural = "stories"
        ordering = ['order']


class Scene(models.Model):
    STATUSES = (
        ('drafting', 'Drafting'),
        ('finished', 'Finished'),
        ('discarded', 'Discarded'),
    )

    title = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='drafting')
    synopsis = models.TextField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    created = models.DateTimeField(default=timezone.now())
    last_modified = models.DateTimeField(default=timezone.now())

    story = models.ForeignKey(Story, related_name='scenes')

    # revisions (from Revision.scene)

    def __unicode__(self):
        title = "{} scene {} ({})".format(self.story.title, self.order, self.title)
        return title

    def __str__(self):
        return self.__unicode__()

    def latest_revision(self):
        if self.revisions.all().count() > 0:
            return self.revisions.order_by('-created').first()
        else:
            return None

    def word_count(self):
        latest_revision = self.latest_revision()

        if latest_revision:
            text = latest_revision.text.strip()
            text = text.replace("\n", " ").replace("  ", " ").strip()

            words = re.split(r"\s+", text)

            if len(words) == 1 and words[0] == '':
                return 0
            else:
                return len(words)
        else:
            return 0

    def title_rendered(self):
        return smartypants.smartypants(self.title)

    def synopsis_rendered(self):
        return smartypants.smartypants(self.synopsis)

    def text(self):
        latest_revision = self.latest_revision()

        if latest_revision:
            return latest_revision.text
        else:
            return ''

    def html(self):
        text = self.text()
        text = text.replace('---', '%%%HR%%%')

        text = mistune.markdown(smartypants.smartypants(text))

        text = text.replace('<p>%%%HR%%%</p>', '<hr/>')

        return text

    def get_neighbor(self, side):
        objects = Scene.objects.filter(story=self.story).exclude(pk=self.pk)
        if side == 'next':
            neighbors = objects.filter(order__gte=self.order).order_by('order')
        else:
            neighbors = objects.filter(order__lte=self.order).order_by('-order')

        if len(neighbors):
            return neighbors[0]
        else:
            return None

    def get_next(self):
        return self.get_neighbor('next')

    def get_prev(self):
        return self.get_neighbor('prev')


class Revision(models.Model):
    text = models.TextField(null=True, blank=True)
    scene = models.ForeignKey(Scene, related_name='revisions')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{}".format(self.created)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-created']


class Draft(models.Model):
    story = models.ForeignKey(Story, related_name='drafts')
    json = models.TextField()
    created = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return "Draft on {}".format(self.created, len(self.json))


class Fragment(models.Model):
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now())
    story = models.ForeignKey(Story, related_name='fragments')

    def __unicode__(self):
        return "{}".format(self.created)

    def html(self):
        text = self.text
        text = text.replace('---', '%%%HR%%%')

        text = mistune.markdown(smartypants.smartypants(text))

        text = text.replace('<p>%%%HR%%%</p>', '<hr/>')

        return text
    class Meta:
        ordering = ['created']


class Character(models.Model):
    name = models.CharField(max_length=300)
    color = models.CharField(max_length=50, default='#000', null=True, blank=True)
    story = models.ForeignKey(Story, related_name='characters')
    scenes = models.ManyToManyField(Scene, related_name='characters')

    def get_random_color(self):
        import math
        import random
        import colorsys

        # Choose a random hue
        hue = random.random()
        r, g, b = colorsys.hsv_to_rgb(hue, 0.47, 0.68)

        # Convert to hex
        r = int(math.ceil(r * 255))
        g = int(math.ceil(g * 255))
        b = int(math.ceil(b * 255))

        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['name']
