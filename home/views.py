from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from .models import Ministry
from .forms import ChurchForm

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'home/index.html', {})

def login(request):
    return render(request, 'home/login.html', {})

def churchForm(request):
    if request.method == 'POST':
        form = ChurchForm(request.POST)
        post = request.POST
        print form.is_valid()
    else:
        form = None
        post = None
    ministries = Ministry.objects.order_by('name')
    context = {
        'ministries': ministries,
        'post': post,
        'form': form
    }
    return render(request, 'home/churchForm.html', context)

def registerChurch(request):
    if(request.POST['password'] != request.POST['confirm']):
        # return render(request, '../templates/home/churchForm.html', {
        #     'input': 'password',
        #     'error_message': "The password does not match",
        # })
        return HttpResponse("Not same password")
    form = ChurchForm(request.POST)
    print form.is_valid()
    return churchForm(request)


    # try:
    #     username = request.POST['username']
    # except (KeyError):
    #     # Redisplay the question voting form.
    #     return render(request, 'form/church.html', {
    #         'input': 'username',
    #         'error_message': "Username is empty",
    #     })
    # else:
    #     try:
    #
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



# def registerVolunteer(request):
#     return render(request, 'home/login.html', {})