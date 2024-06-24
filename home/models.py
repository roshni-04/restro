from django.db import models

# Create your models here.
class Feedback (models.Model):
    #https://docs.djangoproject.com/en/5.0/ref/models/fields/
    c_name= models.CharField(max_length=50)
    c_email= models.CharField(max_length=50)
    c_phno= models.CharField(max_length=50)
    c_desc= models.TextField(null=True)
    fbdate=models.DateField()
    fbid=models.AutoField(primary_key=True)
    is_approved = models.BooleanField(default = False)
    fb_rating = models.IntegerField(default = 1)

    def __str__(self) :
        return self.c_name
    
class Reservation (models.Model):
    #https://docs.djangoproject.com/en/5.0/ref/models/fields/
    c_name= models.CharField(max_length=50)
    c_email= models.CharField(max_length=50)
    c_phno= models.CharField(max_length=50)
    c_desc= models.TextField(null=True)
    rdate=models.DateField()
    rid=models.AutoField(primary_key=True)
    rtime=models.TimeField()
    rppl=models.IntegerField(null=False)
    uid = models.IntegerField(default = 0)  # users who did not login, for them 0

    def __str__(self) :
        return self.c_name