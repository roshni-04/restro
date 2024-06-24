
from django.contrib import admin
from home.models import Feedback, Reservation



class FeedbackAdmin(admin.ModelAdmin):
    #Define the layout for tables in admin login 
    list_display=('c_name','c_email','c_phno')

    
# Register your models here.
#admin.site.register(Feedback)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Reservation)