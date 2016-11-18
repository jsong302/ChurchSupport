from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.template import loader, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from .forms import ChurchForm
import MySQLdb
import json, math

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'home/index.html', {})

# def calc_miles(x):
#     lat = math.asin(math.sin(x) * math.cos(d) + cos(lat1) * sin(d) * cos(tc))
#     dlon = atan2(sin(tc) * sin(d) * cos(lat1), cos(d) - sin(lat1) * sin(lat))
#     lon = mod(lon1 - dlon + pi, 2 * pi) - pi


def search(request):
    if request.method == 'POST':

        zip = request.POST.get('zip')
        response_data = {}
        db = MySQLdb.connect("cso.cb9o8fk82u6u.us-east-1.rds.amazonaws.com", "admin", "noz8VER8!!!", "CSO")
        cursor = db.cursor()
        sql = "SELECT * FROM zipcode WHERE zip=" + zip

        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            response_data['zipcode'] = results[0]
            response_data['lat'] = results[4]
            response_data['long'] = results[5]
        except:
            print "Error: unable to fetch data"

        sql = "SELECT home_church.zip, home_church.name, zipcode.latitude, zipcode.longitude FROM home_church INNER JOIN zipcode ON home_church.zip=zipcode.zip WHERE home_church zip between"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            x = 0
            response_data = [len(results)]
            for row in results:
                response_data[x] = {}
                response_data[x] = {"zipcode": row[0], "name": row[1], "lat": row[2], "lng": row[3]}
                print row[0]
                print row[1]
                print row[2]
                print row[3]
                x = x + 1
            return render(request, 'home/index.html', Context({"markers": response_data}))

        except:
            print "Error: unable to fetch data"
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def login(request):
    return render(request, 'home/login.html', {})

def churchForm(request):
    if request.method == 'POST':
        print "hi1"
        form = ChurchForm(request.POST)
        post = request.POST
        if form.is_valid():
            print "hi2"
            return churchMinForm(request)
    else:
        form = None
        post = None
    # ministries = Ministry.objects.order_by('name')
    context = {
        # 'ministries': ministries,
        'post': post,
        'form': form
    }
    return render(request, 'home/churchForm.html', context)


def churchMinForm(request):
    if request.method == 'POST':
        post = request.POST
        form = request.POST
    else:
        form = None
        post = None
    context = {
        # 'ministries': ministries,
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