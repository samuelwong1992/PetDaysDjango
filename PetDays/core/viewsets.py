from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins, status, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models import Q

import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from .models import PetDaycareRelationship, Profile, Pet, Daycare
from .serializers import DaycareNameSerializer, ProfileSerializer, RegisterSerializer, PetSerializer, PetRequestSerializer, PetDaycareSerializer, DaycareSerializer
from .permissions import IsParent

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
		'request_daycare': PetDaycareSerializer,
	}

	def get_serializer_class(self):
		return self.serializer_classes.get(self.action,
			super().get_serializer_class())

	@action(detail=True,
			methods=['post'],
			url_path='request-daycare',
			permission_classes=[IsParent])
	# @ppsr_list.mapping.patch
	def request_daycare(self, request, *args, **kwargs):
		pet = self.get_object()
		# Get serializer class
		serializer = self.get_serializer_class()
		# Set data
		serializer = serializer(
			data=request.data,
			context={'request': request},
		)
		# Validate data
		serializer.is_valid(raise_exception=True)
		# Save data
		pdr = serializer.save(pet=pet)

		response_serializer = DaycareNameSerializer(pdr.daycare, context={'request': request})
		# Return response
		return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class DaycareFilter(django_filters.FilterSet):
	desc = django_filters.CharFilter(
		method='filter_desc')

	def filter_desc(self, queryset, value, *args, **kwargs):
		if args:
			if len(args) > 0:
				val = args[0]
				queryset = queryset.filter(Q(name__icontains=val) | Q(address__icontains=val))
			return queryset

class DaycareViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = Daycare.objects.all()
	serializer_class = DaycareSerializer
	filter_backends = [
		DjangoFilterBackend,
		filters.SearchFilter,
	]
	filter_class = DaycareFilter
