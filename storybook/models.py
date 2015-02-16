from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Story(models.Model):
    STATUSES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('inactive', 'Inactive'),
    )

    title = models.TextField()
    status = models.CharField(max_length=10, choices=STATUSES)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, default=timezone.now())
    order = models.PositiveSmallIntegerField(default=50000)
    word_count = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.title


class Scene(models.Model):
    STATUSES = (
        ('active', 'Active'),
        ('complete', 'Complete'),
        ('deleted', 'Deleted'),
    )

    title = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES)
    synopsis = models.TextField(null=True, blank=True)
    order = models.PositiveSmallIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, default=timezone.now())

    story = models.ForeignKey(Story, related_name='scenes')

    # revisions (from Revision.scene)

    def __unicode__(self):
        if self.title != "":
            title = self.title
        else:
            title = "Scene {} (untitled)".format(order + 1)

        return title


    def latest_revision(self):
        return self.revisions.order_by('created').first()

class Revision(models.Model):
    text = models.TextField(null=True, blank=True)
    scene = models.ForeignKey(Scene, related_name='revisions')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{}".format(self.created)


class HistoryEntry(models.Model):
    story = models.ForeignKey(Story, related_name='history_entries')
    json = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "History entry on {} of length {}".format(self.created, len(self.json))
