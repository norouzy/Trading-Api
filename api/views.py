from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from extentions.addToWallet import WalletManagment

from pycoingecko import CoinGeckoAPI
from rest_framework import status
from rest_framework.parsers import JSONParser


from .serializers import *

from rest_framework.views import APIView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response

from .permissions import *

from .models import Position, Coin_list

User = get_user_model()


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)


class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)


class PositionList(ListAPIView):
    serializer_class = PositionSerializer
    permission_classes = (IsUser,)

    def get_queryset(self):
        user = self.request.user
        query = Position.objects.filter(paper_trading__user=user)
        return query


class PositionCloseUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = PositionCloseSerializer
    permission_classes = (UserPosition,)

    def get_queryset(self):
        user = self.request.user
        query = Position.objects.filter(paper_trading__user=user)
        return query


class PositionCreate(CreateAPIView):
    serializer_class = PositionAddSerializer

    def perform_create(self, serializer):
        user = self.request.user
        paper = user.paper_trading
        serializer.save(paper_trading=paper)


class PositionTotal(ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsSuperUser,)


class PositionOptionCreate(ListCreateAPIView):
    serializer_class = PositionOptionCreateSerializer
    permission_classes = (UserPositionOption,)

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


class PositionOptionDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PositionOptionUpdateSerializer
    permission_classes = (UserPositionOption,)
    lookup_field = "in_position"

    def get_queryset(self):
        user = self.request.user
        position_id = self.kwargs["in_position"]
        query = Position_option.objects.filter(in_position=position_id, in_position__paper_trading__user=user)
        return query

class PositionOptionClose(RetrieveUpdateDestroyAPIView):
    serializer_class = PositionOptionCloseSerializer
    permission_classes = (UserPositionOption,)
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
    serializer_class = CreatePaperTradingSerializer
    permission_classes = (IsUser,)

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
    serializer_class = UpdatePaperTradingSerializer
    permission_classes = (UserPapertrading,)

    def get_queryset(self):
        user = self.request.user
        query = Paper_trading.objects.filter(user=user)
        return query


class watchList_List(ListCreateAPIView):
    serializer_class = WatchListSerializer
    permission_classes = (IsUser,)

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
    serializer_class = WatchListSerializer
    permission_classes = (UserWatchList,)

    def get_queryset(self):
        user = self.request.user
        query = Watch_list.objects.filter(user=user)
        return query


class walletList(ListAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsUser,)

    def get_queryset(self):
        user = self.request.user
        query = Wallet.objects.filter(paper_trading__user=user)
        return query


from extentions.watchList import WatchList_checker
from extentions.addToWallet import WalletManagment
from extentions.checkPositions import Position_checker
from extentions.checkPositionOption import Position_option_checker
from extentions.validateWallet import ValidateWalletCoin


def test(request):
    # results =WalletManagment.check("btc", -112, request.user)
    # results=WatchList_checker.check("btc","btc",request.user)
    # results=Position_option_checker.check()
    # paper_trading = Paper_trading.objects.filter(user__id=request.user.id)
    # print(paper_trading)
    # print(request.user.id)
    # results = ValidateWalletCoin.check("btc", 0.0010643646871144556, request.user.id)
    results=Position_checker.check()
    return HttpResponse(results)


def socket_test(request):
    data = {'stock1': {'name': 'Stock1', 'opening': 45346, 'closing': 1234, 'currentVal': 56},
            'stock2': {'name': 'Stock2', 'opening': 1889, 'closing': 234235, 'currentVal': 56},
            'stock3': {'name': 'Stock3', 'opening': 1883, 'closing': 5346, 'currentVal': 56},
            'stock4': {'name': 'Stock4', 'opening': 1884, 'closing': 56457, 'currentVal': 56},
            'stock5': {'name': 'Stock5', 'opening': 1881, 'closing': 56457, 'currentVal': 56},

            }
    context = {'data': data, 'tableheader': ['name', 'opening', 'closing', 'currentVal']}
    return render(request, 'index.html', context)


class coinListView(ListCreateAPIView):
    serializer_class = CoinSerializer
    permission_classes = (IsSuperUserOrReadOnly,)
    queryset = Coin_list.objects.all()


    def create(self, request, *args, **kwargs):
        # GET LAST COINS IN DB
        lastCoins = Coin_list.objects.values_list('coin')
        lastCoins = [coin[0] for coin in lastCoins]

        # GET TOTAL CRYPTO COINS
        cg = CoinGeckoAPI()
        data = []
        get_coins = [i['symbol'] for i in cg.get_coins_list()]

        # REMOVE DUPLICATED AND EXISTED COINS
        for elem in get_coins:
            if elem not in lastCoins and len(elem)<20:
                data.append({'coin':elem})

        # SEND DATA TO SERIALIZER
        serializer = self.get_serializer(data=data, many=True)

        # SERIALIZER VALIDATION
        serializer.is_valid(raise_exception=True)

        # CREATE AND SAVE NEW COINS TO DB
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
