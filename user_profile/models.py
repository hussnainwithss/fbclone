import datetime
from django.db import models
from django.conf import settings
from dateutil.relativedelta import relativedelta
# Create your models here.


class City(models.Model):
    """
    City model to store cities for user profile and organizations
    """
    name = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class Organization(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return "{name} @ {location}".format(name=self.name, location=self.city)

    class Meta:
        unique_together = ['name', 'city']


class Education(models.Model):
    school = models.ForeignKey(Organization, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.degree = self.degree.lower()
        self.field = self.field.lower() 
        return super(Education, self).save(*args, **kwargs)

    def __str__(self):
        return "{degree} ({field}) @ {school}".format(degree=self.degree, 
        field=self.field, school=self.school.name)

    class Meta:
        unique_together = ['school', 'degree', 'field','is_completed']


class Work(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    have_left = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.designation = self.designation.lower()
        return super(Work, self).save(*args, **kwargs)

    def __str__(self):
        return "{designation} @ {org}".format(designation=self.designation, org=self.organization)
    
    class Meta:
        unique_together = ['organization','designation','have_left']


class UserProfile(models.Model):
    SINGLE = 'S'
    COMMITTED = 'C'
    MARRIED = 'M'
    DIVORCED = 'D'

    RELATIONSHIP_STATUS_CHOICES = [
        ('S', 'Single'),
        ('C', 'Committed'),
        ('M', 'Married'),
        ('D', 'Divorced')
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    education = models.ManyToManyField(Education, blank=True)
    work = models.ManyToManyField(Work,blank=True)
    birthday = models.DateField()
    hometown = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    relationship_status = models.CharField(
        choices=RELATIONSHIP_STATUS_CHOICES, max_length=1, default=SINGLE)
    def get_age(self):
        return relativedelta(datetime.date.today(), self.birthday)

    def __str__(self):
        return self.user.username
