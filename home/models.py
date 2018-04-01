from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.

APPROVAL_CHOICES = (
    (0, 'Unapproved'),
    (1, 'Approved')
)



class Zipcode(models.Model):
    def __unicode__(self):
        return self.zip
    zip = models.CharField(primary_key=True, max_length=5)
    county = models.TextField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    area_code = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zipcode'

class Location_Area(models.Model):
    def __unicode__(self):
        return 'Location: ' + self.name

    zipcode = models.ForeignKey(Zipcode, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    korean = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

class Church(models.Model):
    def __unicode__(self):
        return self.name[:1] + " Church"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    number = models.CharField(max_length=20, null=True)
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=6, null=True)
    x_lat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)
    y_long = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)
    pastor = models.CharField(max_length=50, null=True)
    pastor_number = models.CharField(max_length=20, null=True)
    church_area1 = models.CharField(max_length=50, null=True, blank=True)
    church_area2 = models.CharField(max_length=50, null=True, blank=True)
    other_language = models.CharField(max_length=50, null=True, blank=True)
    approval = models.PositiveSmallIntegerField(default=0, choices=APPROVAL_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        super(Church, self).save(*args, **kwargs)
        zipcode = Zipcode.objects.get(zip=self.zipcode)
        self.x_lat = zipcode.latitude
        self.y_long = zipcode.longitude
        super(Church, self).save(*args, **kwargs)

class Volunteer(models.Model):
    def __unicode__(self):
        return 'Volunteer: ' + self.user.first_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    address1 = models.CharField(max_length=50, null=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=6, null=True)
    church_name = models.CharField(max_length=50, null=True)
    church_contact = models.CharField(max_length=50, null=True)
    church_phone = models.CharField(max_length=20, null=True)
    approval = models.PositiveSmallIntegerField(default=0, choices=APPROVAL_CHOICES)
    level = models.PositiveSmallIntegerField(null=True, default=5)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

class Min_Group(models.Model):
    def __unicode__(self):
        return 'Group: ' + self.name
    name = models.CharField(max_length=50, null=True)
    icon = models.ImageField(upload_to="icons", null=True, blank=True)

class Min_Category(models.Model):
    def __unicode__(self):
        return 'Category: ' + self.name
    group = models.ForeignKey(Min_Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    korean = models.CharField(max_length=50, null=True, blank=True)
    icon = models.ImageField(upload_to="icons", null=True, blank=True)

class Interest(models.Model):
    def __unicode__(self):
        return 'Volunteer: ' + self.volunteer.user.first_name + ' Category: ' + self.category.name
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    category = models.ForeignKey(Min_Category, on_delete=models.CASCADE)

class Help(models.Model):
    def __unicode__(self):
        return 'Church: ' + self.church.name + ' Category: ' + self.category.name
    category = models.ForeignKey(Min_Category, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, blank=True, null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    students = models.PositiveIntegerField(null=True)
    day = models.PositiveSmallIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

class Help_Request(models.Model):
    def __unicode__(self):
        return self.help.church.name + ": " + self.help.category.group.name + " " + self.help.category.name
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    help = models.ForeignKey(Help, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

