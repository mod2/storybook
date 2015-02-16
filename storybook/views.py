# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response #, get_object_or_404, redirect
import json

#from .models import Story, Scene

#@login_required
def home(request):
    return render_to_response('home.html', { })

#@login_required
def story(request, story_slug):
    return render_to_response('story.html', { 'pagetitle': "Story Title" })
