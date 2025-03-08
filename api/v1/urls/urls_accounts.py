
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include,path
from api.v1.accounts.views import *

router = DefaultRouter()
router.register('login', LoginView, basename='login')
router.register('user_register', UserRegisterView, basename='user_register')
router.register('upload_file', uploadFileView, basename='upload_file')



urlpatterns = [
    path('', include(router.urls)),
    ]