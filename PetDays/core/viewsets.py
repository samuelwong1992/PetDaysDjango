from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import Profile, Pet
from .serializers import ProfileSerializer, RegisterSerializer, PetSerializer, PetRequestSerializer


class LoginViewSet(ObtainAuthToken):
	"""
	Authentication - Login

	Custom login endpoint to return Authentication's key, and
	other user data.

	This endpoint can be called without any data to refresh the
	login data if the user is already authenticated.
	"""

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			profile = Profile.objects.get(user=request.user)
			profileSerializer = ProfileSerializer(
				profile, many=False, context={'request': request})
			token, created = Token.objects.get_or_create(user=request.user)
			return Response({
				'token': token.key,
				'profile': profileSerializer.data
			})

		serializer = self.serializer_class(data=request.data,
											context={'request': request})
		try:
			serializer.is_valid(raise_exception=True)
		except:
			return Response(
				{'error': 'We couldn\'t log you in with those credentials.'})
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)

		try:
			profile = Profile.objects.get(user=user)
			profileSerializer = ProfileSerializer(
				profile, many=False, context={'request': request})
		except:
			return Response(
				{'error': 'It appears like you haven\'t been setup in PetDays'})

		return Response({
			'token': token.key,
			'profile': profileSerializer.data
		})

class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	permission_classes = (AllowAny,)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer_class()
		serializer = serializer(data=request.data,
                                context={'request': request})
		# Validate serializer
		serializer.is_valid(raise_exception=True)
		# Save
		user = serializer.save()

		profile = Profile.objects.get(user=user)
		profileSerializer = ProfileSerializer(
			profile, many=False, context={'request': request})

		token, created = Token.objects.get_or_create(user=user)

		return Response({
			'token': token.key,
			'profile': profileSerializer.data
		})

class PetViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	queryset = Pet.objects.all()
	serializer_class = PetSerializer
	serializer_classes = {
		'create': PetRequestSerializer,
	}

	def get_serializer_class(self):
		return self.serializer_classes.get(self.action,
			super().get_serializer_class())