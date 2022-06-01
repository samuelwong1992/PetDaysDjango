from posixpath import basename
from rest_framework import routers
from django.urls import path, include
from .viewsets import LoginViewSet, RegisterViewSet

api_router = routers.DefaultRouter()
api_router.register('register', RegisterViewSet, basename='auth_register')


urlpatterns = [
    path('', include(api_router.urls)),
	path('login/', LoginViewSet.as_view()),
]