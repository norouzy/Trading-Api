import requests
from django.http import HttpResponse
from django.db import IntegrityError

from .serializers import *
from .permissions import *
from .models import Position, Coin_list

from rest_framework import status, viewsets, serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from extentions.addToWallet import WalletManagment
from extentions.checkPositions import Position_checker
from extentions.checkPositionOption import Position_option_checker


User = get_user_model()


class UserList(ListCreateAPIView):

    """
        Concrete view for listing and create users .
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)


class UserDetail(RetrieveUpdateAPIView):

    """
        Concrete view for read, update or delete specific user .
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)


class PositionList(ListAPIView):

    """
        Concrete view for listing positions.
    """
    serializer_class = PositionSerializer
    permission_classes = (Is_Authenticated, IsUser)

    def get_queryset(self):
        user = self.request.user
        query = Position.objects.filter(paper_trading__user__id=user.id)
        return query


class PositionCloseUpdate(RetrieveUpdateDestroyAPIView):

    """
        Concrete view for read, delete or update(reaching to price or closed) positions.
    """

    serializer_class = PositionCloseSerializer
    permission_classes = (Is_Authenticated, UserPosition,)

    def get_queryset(self):
        user = self.request.user
        query = Position.objects.filter(paper_trading__user__id=user.id)
        return query

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs["pk"]
        position = Position.objects.get(id=id, paper_trading__user=user)
        if not position.status == "w":
            raise serializers.ValidationError("this position reached or closed ! you cant edit it")
        else:
            return self.destroy(request, *args, **kwargs)


class PositionCreate(CreateAPIView):

    """
        Concrete view for create a position.
    """

    serializer_class = PositionAddSerializer
    permission_classes = (Is_Authenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        paper = user.paper_trading
        serializer.save(paper_trading=paper)


class PositionTotal(ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsSuperUser,)


class PositionOptionCreate(ListCreateAPIView):

    """
        Concrete view for listing and create a position option.
    """

    serializer_class = PositionOptionCreateSerializer
    permission_classes = (Is_Authenticated, UserPositionOption,)

    def get_queryset(self):
        user = self.request.user
        id = self.kwargs['pk']
        query = Position_option.objects.filter(in_position=id, in_position__paper_trading__user=user)
        return query

    def perform_create(self, serializer):
        user = self.request.user
        id = self.kwargs['pk']
        position = Position.objects.get(id=id)
        option = Position_option.objects.filter(in_position=position, in_position__paper_trading__user=user)
        if not option:
            serializer.save(in_position=position)
        else:
            raise serializers.ValidationError("You already have a position option")


class PositionOptionUpdate(RetrieveUpdateDestroyAPIView):

    """
        Concrete view for read, update or delete position option .
    """

    serializer_class = PositionOptionUpdateSerializer
    permission_classes = (Is_Authenticated, UserPositionOption,)
    lookup_field = "in_position"

    def get_queryset(self):
        user = self.request.user
        position_id = self.kwargs["in_position"]
        query = Position_option.objects.filter(in_position=position_id, in_position__paper_trading__user=user)
        return query

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        position_id = self.kwargs["in_position"]
        position_option = Position_option.objects.get(in_position=position_id, in_position__paper_trading__user=user)
        if not position_option.status == "w" and not position_option.trade_type == "w" or not position_option.status == "p" and not position_option.status == "w":
            raise serializers.ValidationError("this position reached or closed ! you cant edit it")
        else:
            return self.destroy(request, *args, **kwargs)


class PositionOptionClose(RetrieveUpdateDestroyAPIView):
    serializer_class = PositionOptionCloseSerializer
    permission_classes = (Is_Authenticated, UserPositionOption,)
    lookup_field = "in_position"

    def get_queryset(self):
        user = self.request.user
        position_id = self.kwargs["in_position"]
        query = Position_option.objects.filter(in_position=position_id, in_position__paper_trading__user=user)
        return query


class PapertradingViewSet(viewsets.ModelViewSet):
    serializer_class = CreatePaperTradingSerializer
    permission_classes = (UserPapertrading,)

    def get_queryset(self):
        user = self.request.user
        query = Paper_trading.objects.filter(user=user)
        return query

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class PapertradingListView(ListCreateAPIView):

    """
        Concrete view for listing and create user paper trading.
    """
    serializer_class = CreatePaperTradingSerializer
    permission_classes = (Is_Authenticated, IsUser,)

    def get_queryset(self):
        user = self.request.user
        query = Paper_trading.objects.filter(user=user)
        return query

    def perform_create(self, serializer):
        user = self.request.user

        try:
            serializer.save(user=user)
            paper_trading = Paper_trading.objects.get(user=user)
            WalletManagment.check("usdt", paper_trading.balance, paper_trading)
        except IntegrityError:
            raise serializers.ValidationError("You already have a paper account")


class PapertradingDetail(RetrieveUpdateDestroyAPIView):

    """
        Concrete view for read, update or delete user paper trading.
    """
    serializer_class = UpdatePaperTradingSerializer
    permission_classes = (Is_Authenticated, UserPapertrading,)

    def get_queryset(self):
        user = self.request.user
        query = Paper_trading.objects.filter(user=user)
        return query


class watchList_List(ListCreateAPIView):

    """
        Concrete view for listing and create user watchlist.
    """
    serializer_class = WatchListSerializer
    permission_classes = (Is_Authenticated, IsUser,)

    def get_queryset(self):
        user = self.request.user
        query = Watch_list.objects.filter(user=user)
        return query

    def perform_create(self, serializer):
        user = self.request.user
        try:
            serializer.save(user=user)
        except IntegrityError:
            raise serializers.ValidationError("You already have a paper account")


class watchList_Details(RetrieveDestroyAPIView):

    """
        Concrete view for read or delete user watchlist.
    """
    serializer_class = WatchListSerializer
    permission_classes = (Is_Authenticated, UserWatchList,)

    def get_queryset(self):
        user = self.request.user
        query = Watch_list.objects.filter(user=user)
        return query


class walletList(ListAPIView):

    """
        Concrete view for listing user wallets.
    """

    serializer_class = WalletSerializer
    permission_classes = (Is_Authenticated, IsUser,)

    def get_queryset(self):
        user = self.request.user
        query = Wallet.objects.filter(paper_trading__user=user)
        return query



def positions_checker(request):

    """
        Concrete view function for checking positions to reach .
    """

    results = Position_checker.check()
    return HttpResponse(results)


def options_checker(request):
    results = Position_option_checker.check()
    return HttpResponse(results)


class coinListView(ListCreateAPIView):

    """
        Concrete view for listing coins and update them.
    """

    serializer_class = CoinSerializer
    permission_classes = (IsSuperUserOrReadOnly,)
    queryset = Coin_list.objects.all()

    def create(self, request, *args, **kwargs):
        # GET LAST COINS IN DB
        lastCoins = Coin_list.objects.values_list('coin')
        lastCoins = [coin[0] for coin in lastCoins]

        data = []
        get_coins = []
        url = 'https://min-api.cryptocompare.com/data/all/coinlist'
        res = requests.get(url)
        res = res.json()

        for coin in res['Data']:
            coinName = str(coin).lower()
            get_coins.append(coinName)

        # REMOVE DUPLICATED AND EXISTED COINS
        for elem in get_coins:
            if elem not in lastCoins and len(elem) < 20:
                data.append({'coin': elem})

        # SEND DATA TO SERIALIZER
        serializer = self.get_serializer(data=data, many=True)

        # SERIALIZER VALIDATION
        serializer.is_valid(raise_exception=True)

        # CREATE AND SAVE NEW COINS TO DB
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
