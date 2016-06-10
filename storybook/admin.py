from django.contrib import admin
from .models import Story, Scene, Revision, Draft, Fragment, Character


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'order', 'created', 'last_modified', 'word_count')
    pass


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'created', 'last_modified')
    pass


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ('scene', 'created')
    pass


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('story', 'created')
    pass

@admin.register(Fragment)
class FragmentAdmin(admin.ModelAdmin):
    list_display = ('story', 'created')
    pass

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'story')
    pass
