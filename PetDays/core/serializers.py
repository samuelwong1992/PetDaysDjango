from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Employee, Post, PostPhoto, Profile, Pet, Daycare, PetDaycareRelationship

##################################
#########              ###########
#########   Daycare    ###########
#########              ###########
##################################
class DaycareNameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Daycare
		fields = ('id', 'name')

class DaycareSerializer(serializers.ModelSerializer):
	class Meta:
		model = Daycare
		fields = '__all__'


##################################
#########              ###########
#########     Pet      ###########
#########              ###########
##################################
class PetSerializer(serializers.ModelSerializer):
	daycares = DaycareNameSerializer(many=True, read_only=True)
	
	class Meta:
		model = Pet
		fields = '__all__'

class PetRequestSerializer(PetSerializer):
	def to_internal_value(self, data):
		request = self.context.get('request', None)
		profile = Profile.objects.get(user=request.user)
		value = super().to_internal_value(data)
		value['parent'] = profile
		return value

	class Meta:
		model = Pet
		fields = '__all__'
		extra_kwargs = {
			'parent': {
				'read_only': True,
			}
		}

##################################
#########              ###########
#########  PetDaycare  ###########
######### Relationship ###########
########               ###########
##################################
class PetDaycareSerializer(serializers.ModelSerializer):
	class Meta:
		model = PetDaycareRelationship
		fields = '__all__'
		extra_kwargs = {
			'pet': {'read_only' : True},
		}

##################################
#########              ###########
#########    Profile   ###########
#########              ###########
##################################
class ProfileSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(read_only=True, source="user.first_name")
	last_name = serializers.CharField(read_only=True, source="user.last_name")
	pets = PetSerializer(many=True, read_only=True)
	daycares = serializers.SerializerMethodField()

	@staticmethod
	def get_daycares(obj):
		daycares = obj.get_daycares()
		return DaycareNameSerializer(daycares, many=True).data

	class Meta:
		model = Profile
		fields = ('id', 'first_name', 'last_name', 'profile_picture', 'pets', 'daycares')


##################################
#########              ###########
#########     Auth     ###########
#########              ###########
##################################
class RegisterSerializer(serializers.ModelSerializer) :
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('username', 'password', 'password2', 'first_name', 'last_name')
		extra_kwargs = {
			'first_name': {'required': True},
			'last_name': {'required': True}
		}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})

		return attrs

	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)

		user.set_password(validated_data['password'])
		user.save()

		profile = Profile()
		profile.user = user
		profile.save()

		return user

##################################
#########              ###########
#########   Employee   ###########
#########              ###########
##################################
class EmployeeSerializer(serializers.ModelSerializer):
	daycare = DaycareNameSerializer(many=False, read_only=True)
	first_name = serializers.CharField(read_only=True, source="user.first_name")
	last_name = serializers.CharField(read_only=True, source="user.last_name")
	
	class Meta:
		model = Employee
		fields = ('id', 'first_name', 'last_name', 'daycare', 'profile_picture')

##################################
#########              ###########
#########     Post     ###########
#########              ###########
##################################
class PostPhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostPhoto
		exclude = ('post', )

class PostSerializer(serializers.ModelSerializer):
	daycare = DaycareNameSerializer(many=False, read_only=True)
	employee = EmployeeSerializer(many=False, read_only=True)
	post_photos = PostPhotoSerializer(many=True, read_only=True)
	
	class Meta:
		model = Post
		exclude = ('pets', )