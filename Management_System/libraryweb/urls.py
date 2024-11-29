from django.urls import path
from . import views

app_name = 'libraryweb'

#The names are written so that it can be accessed by any html page using django template tags such as
#url(to get url of webpage) etc

urlpatterns = [
    path('Signin/', views.SignInView.as_view(), name='signin'),
    path('Signup/', views.SignUpView.as_view(), name='signup'),
    path('Signout/', views.sign_out, name='signout'),
    path('Resetpassword/', views.reset_password, name='verify_user'),
    path('<str:lib_num>/Notifications/',views.Notification,name='notifications'),
    path('<str:lib_num>/Request/', views.book_request_view, name='request'),    #Order of url paths matter
    path('<str:lib_num>/Search/', views.SearchPageView.as_view(), name='search'),
    path('<str:lib_num>/Credits/', views.CreditsView.as_view(), name='credits'),
    path('<str:lib_num>/Home/',views.Home_Page,name='home'),
    path('<str:lib_num>/Profile', views.ProfileView.as_view(), name='profile'),
    path('<str:lib_num>/Profile/Updated', views.UpdateProfileView.as_view(), name='update_profile'),
    path('<str:lib_num>/<str:isbn>/', views.DetailPage.as_view(), name="detail"),
    path('<str:lib_num>/Success/<str:isbn>', views.RequestSuccessView.as_view(), name='success'),
    
]


#Future uses
"""path('api/notification-count/', views.notification_count, name='notification_count'),
    path('api/update-notification/', views.update_notification_status, name='update_notification_status'),
"""