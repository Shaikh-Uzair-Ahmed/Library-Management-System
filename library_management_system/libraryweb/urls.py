from django.urls import path
from . import views

app_name = 'libraryweb'

#The names are written so that it can be accessed by any html page using django template tags such as
#url(to get url of webpage) etc

urlpatterns = [
    path('Signin/', views.SignInView.as_view(), name='signin'),
    path('Signup/', views.SignUpView.as_view(), name='signup'),
    path('Forgotpassword/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('Home/',views.Home_Page,name='home'),
    path('Notifications/',views.Notification,name='notifications'),
    path('Request/', views.BookRequestView.as_view(), name='request'),  
    path('Success/', views.RequestSuccessView.as_view(), name='success'),  #Order of url paths matter
    path('Search/', views.SearchPageView.as_view(), name='search'),
    path('Credits/', views.CreditsView.as_view(), name='credits'),
    path('Test500/', views.test_500),
    path('<str:isbn>/', views.DetailPage.as_view(), name="detail"),
    
]


#Future uses
"""path('api/notification-count/', views.notification_count, name='notification_count'),
    path('api/update-notification/', views.update_notification_status, name='update_notification_status'),
"""