import datetime
from django.db import models
from django.conf import settings
from dateutil.relativedelta import relativedelta
# Create your models here.


# class City(models.Model):
#     """
#     City model to store cities for user profile and organizations
#     """
#     name = models.CharField(max_length=255)

#     def save(self, *args, **kwargs):
#         self.name = self.name.lower()
#         return super(City, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.name.title()
#     class Meta:
#         unique_together = ['id','name']




# class Organization(models.Model):
#     name = models.CharField(max_length=255)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)

#     def save(self, *args, **kwargs):
#         self.name = self.name.lower()
#         return super(Organization, self).save(*args, **kwargs)

#     def __str__(self):
#         return "{name} ".format(name=self.name.title())

#     class Meta:
#         unique_together = ['name', 'city']


# class Education(models.Model):
#     school = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     degree = models.CharField(max_length=255)
#     field = models.CharField(max_length=255)
#     is_completed = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         self.degree = self.degree.lower()
#         self.field = self.field.lower() 
#         return super(Education, self).save(*args, **kwargs)

#     def __str__(self):
#         return "{degree} ({field}) @ {school}".format(degree=self.degree.upper(), 
#         field=self.field.title(), school=self.school.name.title())

#     class Meta:
#         unique_together = ['school', 'degree', 'field','is_completed']


# class Work(models.Model):
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     designation = models.CharField(max_length=255)
#     have_left = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         self.designation = self.designation.lower()
#         return super(Work, self).save(*args, **kwargs)

#     def __str__(self):
#         return "{designation} @ {org}".format(designation=self.designation.title(), org=self.organization)
    
#     class Meta:
#         unique_together = ['organization','designation','have_left']


class UserProfile(models.Model):
    SINGLE = 'Single'
    COMMITTED = 'Committed'
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'
    RELATIONSHIP_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Committed', 'Committed'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced')
    ]

    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others','Others')
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="profile")
    bio = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='UserProfiles',blank=True)
    cover_picture = models.ImageField(upload_to='UserProfiles',blank=True)
   
    education = models.CharField(max_length=255, blank=True)
    work = models.CharField(max_length=255,blank=True)
    birthday = models.DateField()
    hometown = models.CharField(max_length=255,blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6,default=FEMALE)
    relationship_status = models.CharField(
        choices=RELATIONSHIP_STATUS_CHOICES, max_length=10, default=SINGLE)
    def get_age(self):
        return relativedelta(datetime.date.today(), self.birthday).years

    def __str__(self):
        return self.user.email
