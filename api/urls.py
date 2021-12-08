from django.urls import path, include
from .views import UserList, UserDetail
app_name = "api"

urlpatterns = [
	path('user/', UserList.as_view(),name="UserList"),
	path('user/<int:pk>', UserDetail.as_view(), name="UserDetail"),
]