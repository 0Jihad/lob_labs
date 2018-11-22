from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    #url = models.TextField(help_text='valid url', default='')
    def publish(self):
        self.published_date = timezone.now()
        self.save()
 
    def __str__(self):
        return self.title
##############################################################################
    

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   photo = models.FileField(verbose_name="Profile Picture", upload_to='archivos', max_length=255, null=True, blank=True)
   website = models.URLField(default='www.wyhh.net', blank=True)
   bio = models.TextField(default='www.wyhh.net', blank=True)
   phone = models.CharField(max_length=20, blank=True, default='08068302532')
   city = models.CharField(max_length=100, default='Ibadan', blank=True)
   country = models.CharField(max_length=100, default='Nigeria', blank=True)
   organization = models.CharField(max_length=100, default='IIRO', blank=True)
   location = models.CharField(max_length=30, default='current location', blank=True)
   birth_date = models.DateField(null=True, blank=True)
   department = models.CharField(max_length=500, blank=True)
   email_confirmed = models.BooleanField(default=False)
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
    instance.profile.save()
    
###############################################################################

from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    department = models.CharField(max_length=500, blank=True)
    
from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
##############################SEARCH############################################

class Students(models.Model):
    student_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=144, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    gpa = models.IntegerField(blank=True, null=True)
    #course_code = models.ForeignKey(Courses, models.DO_NOTHING, db_column='course_code', blank=True, null=True)
    #college = models.ForeignKey(Colleges, models.DO_NOTHING, blank=True, null=True)
    passwords = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        db_table = 'students'