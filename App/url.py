from django.urls import path
from App import views
from .views import get_vessel_details


urlpatterns = [
    path('',views.index_pg, name='signin'),
    path('signup/', views.signup_pg, name='signup'),
    path('usersignup/',views.usersignup_pg, name='usersignup'),
    path('usersignupConf/',views.usersignupConf_pg, name='usersignupconf'),
    path('forgotpass/', views.forgotpass_pg, name='forgotpass'),
    path('resetpasssent/<str:reset_id>/', views.resetpasssent_pg, name='resetpasssent'),
    path('resetpass/<str:reset_id>/', views.resetpass_pg, name='resetpass'),

    path('LineUpForm/',views.LineupForm_pg,name='lineupform'),
    path('AddPortBerth/',views.AddPortBerth_pg,name='addportberth'),
    path('ExtractData/',views.ExtractData_pg,name='extractdata'),
    path('UpdateLineup/<int:id>',views.UpdateLineup_pg,name='UpdateLineup'),

    path('GetCookies/',views.set_cookies,name='getcookies'),
    path('DeleteLineup/<int:id>',views.DeleteLineup_pg,name='DeleteLineup'),
    path('get-berths/', views.get_berths, name='get_berths'),
    path('get-updated-berths/', views.get_updated_berths, name='get_updated_berths'),
    path('get-autocomplete-suggestions/', views.get_autocomplete_suggestions, name='get_autocomplete_suggestions'),
    path('get-vessel-details/', get_vessel_details, name='get_vessel_details'),
]