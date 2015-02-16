from django.contrib import admin
from .models import Story, Scene, Revision, HistoryEntry


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'created', 'last_modified', 'word_count')
    pass


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'created', 'last_modified')
    pass


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ('scene', 'created')
    pass


@admin.register(HistoryEntry)
class HistoryEntryAdmin(admin.ModelAdmin):
    list_display = ('story', 'created')
    pass
