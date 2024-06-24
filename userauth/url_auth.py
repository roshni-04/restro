from .import views
from django.urls import path




urlpatterns = [
   
    path('register/', views.signup_page, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dash/', views.dashboard_page, name='dashboard'),
    path('changepass/', views.changepass_user, name='change-pass'),
    # -------- cuisines ------
    path('addcuisine/', views.add_cuisines, name='add-cuisine'),
    path('showcuisine/', views.show_cuisines, name='show-cuisine'),
    path('editcuisine/<int:cid>/', views.edit_cuisines, name='cuisine-edit'),
    path('deletecuisine/<int:cid>/', views.delete_cuisines, name='cuisine-delete'),
#------menu------------
     path('addmenu/', views.add_menu, name='add-menu'),
    path('showmenu/', views.show_menu, name='show-menu'),
    path('editmenu/<int:mid>/', views.edit_menu, name='menu-edit'),
    path('deletemenu/<int:mid>/', views.delete_menu, name='menu-delete'),
    path('showmenubycat/<int:cid>/', views.menubycat, name='menu-by-cat'),

    # ... SEARCH ...
    
     path('search-results', views.search_results, name='search-results'),
    
 
]
    


