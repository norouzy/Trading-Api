from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from extentions.checkCoin import Coinlist
from extentions.addToWallet import WalletManagment
from extentions.watchList import WatchList_checker

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CreatePaperTradingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        key = list(data)

        if not 'balance' in key and 'enter_balance' in key:

            if data['enter_balance'] > 0.0:

                data.update({'balance': data['enter_balance']})
            else:
                raise serializers.ValidationError("enter balance cant be under zero")
            return data

    class Meta:
        model = Paper_trading
        fields = ["id", "user", 'enter_balance']


class UpdatePaperTradingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        key = list(data)

        if 'balance' in key and not 'enter_balance' in key:
            if data['balance'] >= 0.0:
                return data
            else:
                raise serializers.ValidationError("enter balance cant be under zero")
        else:
            raise serializers.ValidationError("some thing went wrong")

    class Meta:
        model = Paper_trading
        fields = ["id", "user", 'balance']


class PositionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        if Coinlist.check(coin1) and Coinlist.check(coin2):
            return data
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1 == coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
        else:
            raise serializers.ValidationError("coin1 and coin2 not found")

    class Meta:
        model = Position
        fields = "__all__"


class PositionCloseSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='c')

    def validate(self, data):
        data.update({'status': 'c'})
        return data

    class Meta:
        model = Position
        fields = ['status', ]


class PositionAddSerializer(serializers.ModelSerializer):
    paper_trading = serializers.ReadOnlyField(source='paper_trading.id')

    def validate(self, data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        if Coinlist.check(coin1) and Coinlist.check(coin2):
            return data
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1 == coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
        else:
            raise serializers.ValidationError("coin1 and coin2 not found")

    class Meta:
        model = Position
        fields = "__all__"


class PositionOptionSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')

    class Meta:
        model = Position_option
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    paper_trading = serializers.ReadOnlyField(source='paper_trading.id')

    def validate(self, data):
        coin = data['coin']

        if not Coinlist.check(coin):
            raise serializers.ValidationError("coin not found")

        if data['amount'] > 0 and not data['coin'] == None:
            # WalletManagment.ckeck(coin,data['amount'])
            return data

        elif data['amount'] <= 0:
            raise serializers.ValidationError("amount cant be zero or under zero")
        else:
            raise serializers.ValidationError("some thing went wrong")

    class Meta:
        model = Wallet
        fields = "__all__"


class WalletItemSerializer(serializers.ModelSerializer):
    wallet = serializers.ReadOnlyField(source='wallet.id')

    def validate(self, data):
        coin = data['coin']

        if not Coinlist.check(coin):
            raise serializers.ValidationError("coin not found")

        if not data['coin'] == None:
            # WalletManagment.ckeck(coin,data['amount'])
            return data


    class Meta:
        model = WalletItem
        fields = "__all__"


    def create(self, validated_data):
        coin = validated_data['coin']
        amount = validated_data['amount']
        user = self.context.get("user")
        wallet = validated_data["wallet"]

        obj = WalletManagment.check(coin, amount, user, wallet)

        # try:
        #     obj = WalletItem.objects.get(coin=coin, wallet__paper_trading__user=user)
        #     obj.amount += amount
        #     obj.save()
        # except:
        #     obj = WalletItem.objects.create(wallet=wallet, coin=coin, amount=amount)
        #     obj.save()
        return obj


class WatchListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        user = self.context['request'].user

        if not Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 and coin2 not found")
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1 == coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")

        results = WatchList_checker.check(coin1, coin2, user)
        if not results:
            raise serializers.ValidationError("repeative coin")
        return data

    class Meta:
        model = Watch_list
        fields = "__all__"

# WatchListSerializer(
# context={'request': <rest_framework.request.Request: POST '/user/watch-list/'>, 'format': None, 'view': <api.views.watchList_List object>}, data=<QueryDict: {'csrfmiddlewaretoken': ['SLgrcCRfyjcql6TIzNpQiTQCqrQsgmcbqPwtdKuelWElE6MyDX9QrgzI19jE2Zoy'], 'coin': ['cake']}>):
#    id = IntegerField(label='ID', read_only=True)
#    user = ReadOnlyField(source='user.id')
#    coin = CharField(max_length=20)
