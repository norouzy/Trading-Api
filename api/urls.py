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
	path('user/positions/create/', PositionCreate.as_view()),
	path('user/positions/<int:pk>/', PositionCloseUpdate.as_view()),
	path('user/positions/<int:pk>/option/create/', PositionOptionCreate.as_view()),
	path('user/positions/<int:in_position>/option/update/', PositionOptionDetail.as_view()),
	path('user/positions/<int:in_position>/option/close/', PositionOptionClose.as_view()),
	path('user/watch-list/',watchList_List.as_view()),
	path('user/watch-list/<int:pk>/',watchList_Details.as_view()),
	path('user/wallet/',walletList.as_view()),

	path('positions/', PositionTotal.as_view()),
	path('paper-trading/', PapertradingListView.as_view()),
	path('paper-trading/<int:pk>/', PapertradingDetail.as_view()),
	path('test/', test, name="test"),
	path('sokect_test/', socket_test,name="socket_test"),
	path('home/', homeSocketView, name='socket_home'),

	path('coinlist/', coinListView.as_view()),

	path('', include(router.urls))
]
