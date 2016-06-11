from django.contrib import admin
from django import forms

from .models import Story, Scene, Revision, Draft, Fragment, Character

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'order', 'created', 'last_modified', 'word_count')


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'created', 'last_modified', 'story')


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ('scene', 'created')


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('story', 'created')


@admin.register(Fragment)
class FragmentAdmin(admin.ModelAdmin):
    list_display = ('story', 'created')


class CharacterAdminForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [ 'name', 'color', 'story', 'scenes', ]

    def __init__(self, *args, **kwargs):
        super(CharacterAdminForm, self).__init__(*args, **kwargs)

        story = Story.objects.get(id=self.initial['story'])

        self.fields['scenes'].queryset = Scene.objects.filter(story=story)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    form = CharacterAdminForm
    list_display = ('name', 'color', 'story')
    filter_horizontal = ('scenes',)
