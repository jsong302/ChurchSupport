from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import transaction
from django import forms
from home.models import Min_Category, Church, Help, Volunteer
from .forms import ChurchForm, ChurchMinForm, VolunteerForm, VolunteerMinForm
import MySQLdb
import json, math

# Create your views here.
from django.http import HttpResponse


def index(request):
    help = Help.objects.exclude(church__approval = 0)
    response_data = {}
    db = MySQLdb.connect("cso.cb9o8fk82u6u.us-east-1.rds.amazonaws.com", "admin", "noz8VER8!!!", "CSO")
    cursor = db.cursor()

    x = 1
    for h in help:
        h.num = x
        x = x + 1

    context = {
        'help': help
    }
    return render(request, 'home/index.html', context)

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
        form = ChurchForm(request.POST)
        post = request.POST
        print form.is_valid()
        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['username'],
                            password=request.POST['password'], first_name=request.POST['firstName'],
                            last_name=request.POST['lastName'])
                user.save()
                new_church = Church(user=user, name=request.POST['name'], number=request.POST['phone'],
                                    address1=request.POST['address1'], address2=request.POST['address2'],
                                    city=request.POST['city'], state=request.POST['state'], zipcode=request.POST['zipcode'])
                db = MySQLdb.connect("cso.cb9o8fk82u6u.us-east-1.rds.amazonaws.com", "admin", "noz8VER8!!!", "CSO")
                cursor = db.cursor()
                sql = "SELECT * FROM zipcode WHERE zip=" + request.POST['zipcode']
                try:
                    cursor.execute(sql)
                    results = cursor.fetchone()
                    new_church.x_lat = results[4]
                    new_church.y_long = results[5]
                except:
                    print "Error: unable to fetch data"
                new_church.save()
                return HttpResponseRedirect(reverse('home:churchMinForm', args=[new_church.id]))
                # return redirect('churchMinForm', church_id = new_church.id)



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


def churchMinForm(request, id):
    ministries = Min_Category.objects.order_by('name')
    print request.method
    if request.method == 'POST':
        form = ChurchMinForm(request.POST)
        post = request.POST
        count = request.POST['count']
        print count
        for x in range(0, int(count) + 1):
            with transaction.atomic():
                try:
                    category = Min_Category.objects.get(id=request.POST["category[" + str(x) + "]"])
                    church = Church.objects.get(id=id)
                    help = Help(category=category, church=church, start=request.POST["start[" + str(x) + "]"],
                                end=request.POST["end[" + str(x) + "]"], students=request.POST["students[" + str(x) + "]"],
                                day=request.POST["day[" + str(x) + "]"])
                    help.save()
                except KeyError:
                    print "KeyError in index: " + str(x)
    else:
        form = None
        post = None

    context = {
        'ministries': ministries,
        'post': post,
        'form': form,
        'id': id
    }
    return render(request, 'home/churchMinForm.html', context)

# def registerChurch(request):
#     if(request.POST['password'] != request.POST['confirm']):
#         # return render(request, '../templates/home/churchForm.html', {
#         #     'input': 'password',
#         #     'error_message': "The password does not match",
#         # })
#         return HttpResponse("Not same password")
#     form = ChurchForm(request.POST)
#     print form.is_valid()
#     return churchForm(request)

def volunteerForm(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        post = request.POST
        if form.is_valid():
            print post
            with transaction.atomic():
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['username'],
                                                password=request.POST['password'], first_name=request.POST['firstName'],
                                                last_name=request.POST['lastName'])
                user.save()
                new_vol = Volunteer(user=user, phone=request.POST['phone'],
                                    address1=request.POST['address1'], address2=request.POST['address2'],
                                    city=request.POST['city'], state=request.POST['state'],
                                    zipcode=request.POST['zipcode'], church_name=request.POST['churchName'],
                                    church_contact=request.POST['contactName'], church_phone=request.POST['contactPhone'])
                new_vol.save()
                return HttpResponseRedirect(reverse('home:index'))
                # return HttpResponseRedirect(reverse('home:volunteerMinForm', args=[new_vol.id]))
                # return redirect('churchMinForm', church_id = new_church.id)
    else:
        form = None
        post = None
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'home/volunteerForm.html', context)

def volunteerMinForm(request, id):
    if request.method == 'POST':
        form = VolunteerMinForm(request.POST)
        post = request.POST
        print post
    else:
        form = None
        post = None
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'home/volunteerMinForm.html', context)


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