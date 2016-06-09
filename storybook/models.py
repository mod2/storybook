from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField

import mistune
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
        if self.title != "":
            title = self.title
        else:
            title = "Scene {} (untitled)".format(order + 1)

        return title


    def latest_revision(self):
        if self.revisions.all().count() > 0:
            return self.revisions.order_by('-created').first()
        else:
            return None

    def word_count(self):
        latest_revision = self.latest_revision()
        if latest_revision:
            # TODO: this doesn't actually work (newlines, etc.)
            return len(latest_revision.text.split(' '))
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
        return mistune.markdown(smartypants.smartypants(self.text()))


class Revision(models.Model):
    text = models.TextField(null=True, blank=True)
    scene = models.ForeignKey(Scene, related_name='revisions')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{}".format(self.created)

    class Meta:
        ordering = ['-created']


class HistoryEntry(models.Model):
    story = models.ForeignKey(Story, related_name='history_entries')
    json = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "History entry on {} of length {}".format(self.created, len(self.json))

    class Meta:
        verbose_name_plural = "history entries"
