from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from django.contrib.auth import authenticate, login, logout
from home.models import Min_Category, Church, Help, Volunteer, Help_Request, Interest, Zipcode
from .forms import ChurchForm, ChurchMinForm, VolunteerForm, VolunteerMinForm, LoginForm
import MySQLdb
import json, math

# Create your views here.
from django.http import HttpResponse


def not_in_church_group(user):
    return user.is_authenticated() and user.groups.filter(name='Church').exists()

def not_in_volunteer_group(user):
    return user.is_authenticated() and user.groups.filter(name='Church').exists()


def index(request):
    help = Help.objects.exclude(church__approval = 0).extra(order_by = ['church__city'])
    response_data = {}

    x = 1
    lookup = dict()

    for h in help:
        key = h.church.zipcode
        h.church.name = h.church.name[:1] + " Church"
        if key in lookup:
            h.num = lookup[key]
        else:
            h.num = x
            lookup[key] = x
            x += 1

    context = {
        'help': help
    }
    return render(request, 'home/index.html', context)

# def calc_miles(x):
#     lat = math.asin(math.sin(x) * math.cos(d) + cos(lat1) * sin(d) * cos(tc))
#     dlon = atan2(sin(tc) * sin(d) * cos(lat1), cos(d) - sin(lat1) * sin(lat))
#     lon = mod(lon1 - dlon + pi, 2 * pi) - pi


# def search(request):
#     if request.method == 'POST':
#
#         zip = request.POST.get('zip')
#         response_data = {}
#         db = MySQLdb.connect("cso.cb9o8fk82u6u.us-east-1.rds.amazonaws.com", "admin", "noz8VER8!!!", "CSO")
#         cursor = db.cursor()
#         sql = "SELECT * FROM zipcode WHERE zip=" + zip
#
#         try:
#             cursor.execute(sql)
#             results = cursor.fetchone()
#             response_data['zipcode'] = results[0]
#             response_data['lat'] = results[4]
#             response_data['long'] = results[5]
#         except:
#             print "Error: unable to fetch data"
#
#         sql = "SELECT home_church.zip, home_church.name, zipcode.latitude, zipcode.longitude FROM home_church INNER JOIN zipcode ON home_church.zip=zipcode.zip WHERE home_church zip between"
#         try:
#             cursor.execute(sql)
#             results = cursor.fetchall()
#             x = 0
#             response_data = [len(results)]
#             for row in results:
#                 response_data[x] = {}
#                 response_data[x] = {"zipcode": row[0], "name": row[1], "lat": row[2], "lng": row[3]}
#                 print row[0]
#                 print row[1]
#                 print row[2]
#                 print row[3]
#                 x = x + 1
#             return render(request, 'home/index.html', Context({"markers": response_data}))
#
#         except:
#             print "Error: unable to fetch data"
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )

def userLogin(request):
    if request.method == 'POST':
        post = request.POST
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home:index'))
                else:
                    form.add_error(None, "This account has been disabled")
            else:
                form.add_error(None, "Invalid User")
    else:
        post = None
        form = LoginForm()
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'home/login.html', context)

def userLogout(request):

    logout(request)

    return HttpResponseRedirect(reverse('home:index'))

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
                                    city=request.POST['city'], state=request.POST['state'], zipcode=request.POST['zipcode'],
                                    pastor=request.POST['pastor'], pastor_number=request.POST['pastorPhone'])
                zipcode = Zipcode.objects.get(zip=request.POST["zipcode"])
                new_church.x_lat = zipcode.latitude
                new_church.y_long = zipcode.longitude
                new_church.save()
                group = Group.objects.get(name='Church')
                group.user_set.add(user)
                u = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, u)
                return HttpResponseRedirect(reverse('home:churchMinForm'))



    else:
        form = None
        post = None
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'home/churchForm.html', context)

@login_required(redirect_field_name=None)
@user_passes_test(not_in_church_group, login_url='/login/', redirect_field_name=None)
def churchMinForm(request):
    ministries = Min_Category.objects.order_by('name')
    church = Church.objects.get(user = request.user)
    requests = Help.objects.all().filter(church=church)
    print requests
    if request.method == 'POST':
        form = ChurchMinForm(request.POST)
        post = request.POST
        count = request.POST['count']
        print count
        for x in range(0, int(count) + 1):
            with transaction.atomic():
                try:
                    category = Min_Category.objects.get(id=request.POST["category[" + str(x) + "]"])
                    church = Church.objects.get(id=church.id)
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
        'requests': requests
    }
    return render(request, 'home/churchMinForm.html', context)

@login_required(redirect_field_name=None)
@user_passes_test(not_in_church_group, login_url='/login/', redirect_field_name=None)
def removeHelp(request, id):
    help = Help.objects.get(id=id)
    if help.church.user == request.user:
        help.delete()
        return HttpResponseRedirect(reverse('home:churchMinForm'))
    else:
        return HttpResponseRedirect(reverse('home:login'))


def volunteerForm(request, id = None):
    if id:
        help = True
    else:
        help = False
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        post = request.POST
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=request.POST['username'], email=request.POST['username'],
                                                    password=request.POST['password'],
                                                    first_name=request.POST['firstName'],
                                                    last_name=request.POST['lastName'])
                    user.save()
                    new_vol = Volunteer(user=user, phone=request.POST['phone'],
                                        address1=request.POST['address1'], address2=request.POST['address2'],
                                        city=request.POST['city'], state=request.POST['state'],
                                        zipcode=request.POST['zipcode'], church_name=request.POST['churchName'],
                                        church_contact=request.POST['contactName'],
                                        church_phone=request.POST['contactPhone'])
                    new_vol.save()
                    if id:
                        return HttpResponseRedirect(reverse('home:helpConfirm', args=[id, new_vol.id]))
                    else:
                        return HttpResponseRedirect(reverse('home:volunteerMinForm', args=[new_vol.id]))
            except IntegrityError as e:
                form.add_error(None, "This email is already taken.")


    else:
        form = None
        post = None

    if id:
        context = {
            'post': post,
            'form': form,
            'id': id,
            'help': help
        }
    else:
        context = {
            'post': post,
            'form': form,
            'help': help
        }
    return render(request, 'home/volunteerForm.html', context)

def volunteerMinForm(request, id):
    ministries = Min_Category.objects.order_by('name')
    if request.method == 'POST':
        form = VolunteerMinForm(request.POST)
        post = request.POST
        count = request.POST['count']
        print count
        for x in range(0, int(count) + 1):
            with transaction.atomic():
                try:
                    category = Min_Category.objects.get(id=request.POST["category[" + str(x) + "]"])
                    volunteer = Volunteer.objects.get(id=id)
                    interest = Interest(category=category, volunteer=volunteer)
                    interest.save()
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
    return render(request, 'home/volunteerMinForm.html', context)



def helpConfirm(request, id, vol):
    help = Help.objects.get(id=id)
    if request.method == 'POST':
        post = request.POST
        print post
    else:
        post = None

    context = {
        'post': post,
        'help': help,
        'vol': vol
    }
    return render(request, 'home/helpConfirm.html', context)

def submitRequest(request):
    if request.method == 'POST':
        post = request.POST
        with transaction.atomic():
            help = Help.objects.get(id=request.POST["help_id"])
            vol = Volunteer.objects.get(id=request.POST["volunteer_id"])
            request = Help_Request(help=help, volunteer=vol)

            request.save()
            # return HttpResponseRedirect(reverse('home:index'))
            return HttpResponseRedirect(reverse('home:volunteerMinForm', args=[vol.id]))
                # return redirect('churchMinForm', church_id = new_church.id)
    else:
        return HttpResponseRedirect(reverse('home:volunteerMinForm', args=[request.POST["volunteer_id"]]))



# def registerVolunteer(request):
#     return render(request, 'home/login.html', {})