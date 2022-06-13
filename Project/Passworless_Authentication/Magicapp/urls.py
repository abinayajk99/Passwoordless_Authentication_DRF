from django.contrib import admin
from django.urls import path,include
from Magicapp.views import (
    SignupView,
    SigninView
)

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    # path('signin/<str:email>/<int:token>',SigninView.as_view(),name="signup"),
    path('signin',SigninView.as_view(),name="signup")
]
