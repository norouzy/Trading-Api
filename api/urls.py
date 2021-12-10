from django.urls import path, include
from .views import UserList, UserDetail, Positionlist, PositionAdd
app_name = "api"

urlpatterns = [
	path('user/', UserList.as_view(),name="UserList"),
	path('user/<int:pk>', UserDetail.as_view(), name="UserDetail"),
	path('user/position/list/', Positionlist.as_view(), name="Positionlist"),
	path('user/position/add/', PositionAdd.as_view(), name="PositionAdd"),
]