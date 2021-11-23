from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		# fields = "__all__"
		# exclude= ['is_superuser','is_staff','is_active','date_joined','user_permissions','groups']
		fields = ['username', 'first_name','last_name','email']