from . import views
from django.urls import path

urlpatterns = [
    path('hello/', views.say_hello),
    path('', views.indexpage),
    path('home/', views.indexpage, name='home'),
    path('test/', views.test),
    path('neworder/', views.neworder),
    path('feedback/', views.feedbackpage),
    path('feedbackshow/', views.allfeedbacks),
    path('feedbackedit/<int:fbnum>/', views.editFeedback,name='feedback-edit'),
    path('feedbackdelete/<int:fbnum>/', views.deleteFeedback,name='feedback-delete'),
    path('feedbackapprove/', views.approve_feedback, name='approve-feedback'),

    path('booktable/', views.booktable,name='book-table'),
    path('showreservation/', views.showreservation,name='show-reservation'),
    path('reservationedit/<int:rnum>/', views.editReservation,name='reservation-edit'),
    path('reservationdelete/<int:rnum>/', views.deleteReservation,name='reservation-delete'),

    path('getpdf/', views.booking_pdffile, name='get-pdf'),
    path('getcsv/', views.booking_csvfile, name='get-csv'),
    path('gettext/', views.booking_txtfile, name='get-text'),
]

