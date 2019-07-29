from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from user_auth_app import views

router = DefaultRouter()

urlpatterns = [

]
router.register('user', views.UserViewSet)
router.register('verity', views.VerityViewSet)
router.register('code', views.SmsCodeViewset, base_name="code")
router.register('usersRegister', views.UserRegisterViewset, base_name="users")
urlpatterns += router.urls