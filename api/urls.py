from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = "api"


urlpatterns = [
	path('user/', UserList.as_view(),name="UserList"),
	path('user/<int:pk>', UserDetail.as_view(), name="UserDetail"),

	path('user/positions/', PositionList.as_view()),
	path('user/positions/<int:pk>/', PositionStatusUpdate.as_view()),
	path('user/positions/create/', PositionCreate.as_view()),

	path('positions/', PositionTotal.as_view()),
	path('paper-trading/', PapertradingListView.as_view()),
]
