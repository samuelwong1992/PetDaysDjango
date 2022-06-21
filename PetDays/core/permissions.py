from rest_framework import permissions

from .models import Profile

class IsParent(permissions.BasePermission):
	"""
	Allow users who is the parent
	"""
	def has_object_permission(self, request, view, obj):
		# Return boolean of user's dealership
		if request.user.is_authenticated:
			profile = Profile.objects.get(user=request.user)
			return obj.parent==profile
		else :
			return False