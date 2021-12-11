from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = "api"

router = routers.SimpleRouter()
router.register('paper-tradingg', PapertradingViewSet, basename='paper_trading')

urlpatterns = [
	path('user/', UserList.as_view(),name="UserList"),
	path('user/<int:pk>', UserDetail.as_view(), name="UserDetail"),

	path('user/positions/', PositionList.as_view()),
	path('user/positions/<int:pk>/', PositionStatusUpdate.as_view()),
	path('user/positions/<int:pk>/option/', PositionOption.as_view()),
	path('user/positions/create/', PositionCreate.as_view()),

	path('positions/', PositionTotal.as_view()),
	path('paper-trading/', PapertradingListView.as_view()),
	path('paper-trading/<int:pk>/', PapertradingDetail.as_view()),

	path('', include(router.urls))
]
