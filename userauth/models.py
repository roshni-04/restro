from django.db import models

from userauth.utilities import get_file_path

#---- cuisine category ---
class Cuisine (models.Model):
    name= models.CharField(max_length=50)
    desc= models.TextField()
    # img = models.ImageField(null = True, blank = True, upload_to='images/')
    img = models.ImageField(null = True, blank = True, upload_to=get_file_path)
    
    
    def __str__(self) :
        return self.name

# ------ Menu Items ------
class MenuItem(models.Model):
    menu_id= models.AutoField(primary_key = True)
    name= models.CharField(max_length=50)
    desc= models.TextField()
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    cuisine_cat = models.ForeignKey(Cuisine, on_delete=models.CASCADE, default = 1)  # maps the fkey to the Primary Key of the Cuisine table

    def __str__(self) :
        return self.name