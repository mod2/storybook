from django.contrib import admin
from django import forms

from .models import Story, Scene, Draft, Inbox, InboxEntry

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'order', 'created', 'last_modified', 'word_count')


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'story', 'word_count', 'created', 'last_modified', 'order')


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('story', 'created')


@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(InboxEntry)
class InboxEntryAdmin(admin.ModelAdmin):
    list_display = ('text', 'created',)
