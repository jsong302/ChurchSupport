from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from home.models import Ministry

# Create your views here.
