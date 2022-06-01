from django.db import models
from django.contrib.auth.models import User
from .image_helpers import images_filename_generator

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to=images_filename_generator)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

class Daycare(models.Model):
	name = models.CharField(max_length=255, blank=True)
	
	def __str__(self):
		return self.name


class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	daycare = models.ForeignKey(Daycare, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	profile_picture = models.ImageField(upload_to=images_filename_generator)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

class Pet(models.Model):
	name = models.CharField(max_length=255)
	parent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pets')
	daycares = models.ManyToManyField(Daycare)
	profile_picture = models.ImageField(upload_to=images_filename_generator)

	def __str__(self):
		return self.name

class Post(models.Model):
	daycare = models.ForeignKey(Daycare, on_delete=models.CASCADE)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	pets = models.ManyToManyField(Pet)
	date_time_created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	def __str__(self):
		return str(self.daycare)

class PostPhoto(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	is_vin = models.BooleanField(default=False)
	photo = models.ImageField(upload_to=images_filename_generator)

	def __str__(self):
		return str(self.post)