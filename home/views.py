import csv
import io
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from home.models import Feedback, Reservation
from datetime import date
#---- for messages framework ---
from django.contrib import messages

from userauth.models import Cuisine
from userauth import utilities

#--------import for pdf file generation
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def say_hello(request):
    """We can perform all sorts of controller activities here such as pull data from database, tranform data, send emails etc"""
    return HttpResponse('Hello World')

def indexpage(request):
    cuisine_list = Cuisine.objects.all()
    return render(request,'index.html', {'cuisines' : cuisine_list})

def test(request):
    context={"name":"Shraddha", "roll":"77"} #pass additional data to the page in the form of a mapping or dictionary
    return render(request,'test.html',context)

def neworder(request):
    
    return render(request,'neworder.html')

def feedbackpage(request):
    if request.method == "POST":
        cname = request.POST.get('txtName')
        cphone = request.POST.get('txtPhone')
        cemail = request.POST.get('txtEmail')
        fbdesc = request.POST.get('txtDesc')
        fbrating = request.POST.get('rating')

        fbObj = Feedback(c_name = cname, c_email = cemail, c_phno = cphone, c_desc = fbdesc, fbdate = date.today(), fb_rating = fbrating)

        fbObj.save()

        messages.success(request, 'Feedback submitted successfully')

        # print(cname, ' - ', cphone, ' - ', cemail, ' - ', fbdesc)
    return render(request,'feedback.html')

def allfeedbacks(request):
    allfb=Feedback.objects.filter(is_approved=True) # show only the approved feedback
    context1={"feedbacks":allfb}
    return render(request,'allfeedbacks.html',context1) 

def editFeedback(request,fbnum):
    selectedfb=Feedback.objects.get(fbid=fbnum)
    context2={"selected_feedback":selectedfb}
    if request.method == "POST":
        cname = request.POST.get('txtName')
        cphone = request.POST.get('txtPhone')
        cemail = request.POST.get('txtEmail')
        fbdesc = request.POST.get('txtDesc')
        fbrating = request.POST.get('rating')

        selectedfb.c_name=cname
        selectedfb.c_phno=cphone
        selectedfb.c_email=cemail
        selectedfb.c_desc=fbdesc
        selectedfb.fb_rating = fbrating

        selectedfb.save()

        messages.success(request, 'Feedback updated successfully')
        return redirect('/restroapp/feedbackshow')
    return render(request,'editfeedback.html',context2)


def deleteFeedback(request, fbnum):
    # Grab the object details which is under process
    selectedfb =    Feedback.objects.get(fbid = fbnum) # ****** where id = 1
    selectedfb.delete()

    messages.info(request, 'Feedback deleted successfully')
    return redirect('/restroapp/feedbackshow')

def approve_feedback(request):
    if request.method=="POST":
        fb_id = request.POST['fbk_id']
        fbObj = Feedback.objects.get(fbid = fb_id)
        fbObj.is_approved = not fbObj.is_approved
        fbObj.save()

        return JsonResponse({'status': 1})


#-------------------------------------------------------
#       RESRVATION
#-------------------------------------------------------
def booktable(request):
    if request.method == "POST":
        cname = request.POST.get('txtName')
        cphone = request.POST.get('txtPhone')
        cemail = request.POST.get('txtEmail')
        rdesc = request.POST.get('txtDesc')
        cdate=request.POST.get('txtDate')
        ctime=request.POST.get('txtTime')
        cppl=request.POST.get('txtPplcount')

        usrid = 0
        if request.user.is_authenticated:
            usrid = request.user.id

        rObj = Reservation(c_name = cname, c_email = cemail, c_phno = cphone, c_desc = rdesc, rdate = cdate,rtime=ctime,rppl=cppl, uid = usrid)

        rObj.save()

        subject="Reservation at EatIt"
        msg=""" Hello! %s , your booking at our place is confirmed. WE will be expecting you on %s at %s.
        \n  Thank you for your interest.
        \n\n Regards,
        \n - Team EatIt"""% (cname,cdate,ctime)
        utilities.send_custom_email(subject,msg,cemail)

        messages.success(request, 'Reservation made successfully')
    return render(request,'reservation/newbooking.html')


def showreservation(request):
  
    allres = None
    if request.user.is_authenticated:
        if request.user.is_staff:
            allres=Reservation.objects.all()
        else:
            userid = request.user.id
            allres = allres=Reservation.objects.filter(uid = userid)
    
        
        context1={"feedbacks":allres}
        return render(request,'reservation/showreservation.html',context1)
    else:
        messages.warning(request, 'You must login to access this page.')
        return redirect('/restroapp/login')

def editReservation(request,rnum):
    

    selectedres=Reservation.objects.get(rid=rnum)

    if not request.user.is_staff and selectedres.uid != request.user.id:
        messages.warning(request, "You are not authorized to access this page")
        return redirect('show-reservation')

    context2={"selected_reservation":selectedres}

    if request.method == "POST":
        cname = request.POST.get('txtName')
        cphone = request.POST.get('txtPhone')
        cemail = request.POST.get('txtEmail')
        cdate = request.POST.get('txtDate')
        ctime = request.POST.get('txtTime')
        cppl = request.POST.get('txtPplcount')
        cdesc = request.POST.get('txtDesc')
       
        selectedres.c_name=cname
        selectedres.c_phno=cphone
        selectedres.c_email=cemail
        selectedres.rdate=cdate
        selectedres.rtime=ctime
        selectedres.rppl=cppl
        selectedres.c_desc=cdesc
       

        selectedres.save()

        messages.success(request, 'Reservation updated successfully')
        return redirect('/restroapp/showreservation')
    
    return render(request,'reservation/editreservation.html',context2)


def deleteReservation(request, rnum):
    # Grab the object details which is under process
    selectedres =   Reservation.objects.get(rid = rnum) # ****** where id = 1

    if not request.user.is_staff and selectedres.uid != request.user.id:
        messages.warning(request, "You are not authorized to access this page")
        return redirect('show-reservation')

    selectedres.delete()

    messages.info(request, 'Reservation deleted successfully')
    return redirect('/restroapp/showreservation')

#------------------------------------------------------------
#       PRINTING & saving data
#---------------------------------------------------------

#----------------------------------------------------------
#    Generate pdf with list of orders using ReportLab
#   https://www.reportlab.com/docs/reportlab-userguide.pdf
#----------------------------------------------------------

def booking_pdffile(request):
    # create a ByteStream buffer
    buff = io.BytesIO()
    # # Create a canvas
    can = canvas.Canvas(buff, pagesize=letter, bottomup = 0) # Letter size page
    # # create a text object
    txtObj = can.beginText()
    txtObj.setTextOrigin(inch, inch)
    txtObj.setFont("Helvetica", 14)

    # add some lines of text
    """
    txtlines = [
        "This is line 1", 
        "This is line 2", 
        "This is line 3", 
        "This is line 4", 
    ] """
    txtlines = []

    # orderlist = Orders.objects.all()
    if request.user.is_staff:  # show all for staff user
        booking_list = Reservation.objects.all()
    else:
        booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

    for rv in booking_list:
        # txtlines.append(rv.cname)
        # txtlines.append(rv.cemail)
        # txtlines.append(rv.cphn)
        # txtlines.append(str(rv.rv_date))
        # txtlines.append(str(rv.rv_time))
        # txtlines.append(str(rv.ppl_count))
        # txtlines.append(rv.msg)

        txtlines.append(rv.c_name  + ' | ' + rv.c_email  + ' | ' + rv.c_phno  + ' | ' + str(rv.rdate)  + ' at ' + str(rv.rtime)  + ' | ' + str(rv.rppl) + '|')
        txtlines.append("=======================================================================================================================================================")

    # Loop
    for line in txtlines:
        txtObj.textLine(line)

    # finish up
    can.drawText(txtObj)
    can.showPage()
    can.save()
    buff.seek(0)

    # return response
    return FileResponse(buff, as_attachment=True, filename='orders.pdf') 
                    # -----------utilities.get_file_path(filename='orders.pdf')

#----------------------------------------------------------
#    Generate csv with list of orders
#----------------------------------------------------------
def booking_csvfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=booking.csv'

    # create a CSV writer
    writer = csv.writer(response)

    if request.user.is_staff:  # show all for staff user
        booking_list = Reservation.objects.all()
    else:
        booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

    # Add column headings to the csv
    writer.writerow(['Customer name', 'e-mail ', 'Phone #', 'Booking Date', 'Booking time', '# of people', 'Message'])  # pass a list of column values

    # write all records
    for rv in booking_list:
        writer.writerow([rv.c_name, rv.c_email, rv.c_phno, rv.rdate, rv.rtime, rv.rppl, rv.c_desc])

    return response

#----------------------------------------------------------
#    Generate text file with list of orders
#----------------------------------------------------------
def booking_txtfile(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=orders.txt'

    txtlines = []

    if request.user.is_staff:  # show all for staff user
        booking_list = Reservation.objects.all()
    else:
        booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

    for rv in booking_list:
        txtlines.append(f'{rv.c_name} | {rv.c_email} | {rv.c_phno} | {rv.rdate} | {rv.rtime} | {rv.rppl} | {rv.c_desc}\n')

    response.writelines(txtlines)
    return response
