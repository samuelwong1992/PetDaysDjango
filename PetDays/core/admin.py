from django.contrib import admin
from .models import Profile, Daycare, Employee, Pet, Post, PostPhoto

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('__str__', )

@admin.register(Daycare)
class DaycareAdmin(admin.ModelAdmin):
	list_display = ('__str__', )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('__str__', )

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
	list_display = ('__str__', )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('__str__', )

@admin.register(PostPhoto)
class PostPhotoAdmin(admin.ModelAdmin):
	list_display = ('__str__', )
