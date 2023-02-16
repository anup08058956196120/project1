from django.contrib import admin
from django.urls import path
from demoapp import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('savedata/',views.savedata),
    path('checkUsername/',views.checkUsername),
    # path('register/',views.register),
    path('register/',views.showregister),
    
    path('',views.homepage),
    path('login/',views.login),
    path('next/',views.next),
    path('previous/',views.previous),
    path('end/',views.endpage),
    path('score/',views.result),
    path('storeans/',views.storeans),
    path('answerschecking/',views.answerschecking),
    path('viewQuestion/',views.viewQuestion),
    path('saveQuestions/',views.saveQuestions),
    path('updateQuestion/',views.updateQuestion),
    path('deleteQuestion/',views.deleteQuestion),
    path('adminpage/',views.adminpage),
    
    
    
    

    
    
    
    
]


