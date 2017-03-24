from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField

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
    status = models.CharField(max_length=10, choices=STATUSES,
                              default=STATUSES[0][0])
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    order = models.PositiveSmallIntegerField(default=50)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def version(self):
        return str(self.drafts.count()).zfill(3)

    def word_count(self):
        word_count = 0

        for scene in self.scenes.all():
            word_count += scene.word_count

        return word_count


    class Meta:
        verbose_name_plural = "stories"
        ordering = ['order']


class Scene(models.Model):
    title = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)

    word_count = models.PositiveIntegerField(default=0)

    order = models.PositiveSmallIntegerField(default=1)

    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)

    story = models.ForeignKey(Story, related_name='scenes')

    def __unicode__(self):
        title = "{} scene {} ({})".format(self.story.title, self.order, self.title)
        return title

    def __str__(self):
        return self.__unicode__()

    def title_rendered(self):
        return smartypants.smartypants(self.title)

    def edit_text(self):
        return '## {}\n\n{}'.format(self.title, self.text)

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


class Draft(models.Model):
    story = models.ForeignKey(Story, related_name='drafts')
    story_text = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.story_text

    class Meta:
        ordering = ['created']


class Fragment(models.Model):
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
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


