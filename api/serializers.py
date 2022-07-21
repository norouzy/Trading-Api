from rest_framework import serializers

from extentions.checkCoin import Coinlist
from extentions.validateWallet import ValidateWalletCoin
from extentions.addToWallet import WalletManagment
from extentions.CoinPrice import PriceChecker
from extentions.watchList import WatchList_checker

from .models import *


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email']


class CreatePaperTradingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        key = list(data)
        if not 'balance' in key and 'enter_balance' in key:
            
            if data['enter_balance']>0.0:
                
                data.update({'balance':data['enter_balance']})
            else:
                raise serializers.ValidationError("enter balance cant be under zero")
            return data

    class Meta:
        model = Paper_trading
        fields = ["id","user", 'enter_balance']


class UpdatePaperTradingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        key = list(data)

        if 'enter_balance' in key and not 'balance' in key:
            if data['enter_balance'] >= 0.0:
                user = self.context['request'].user
                user_paper_trading = Paper_trading.objects.get(user=user)
                data.update({'enter_balance':data['enter_balance'] + user_paper_trading.enter_balance})
                return data
            else:
                raise serializers.ValidationError("enter balance cant be under zero")
        else:
            raise serializers.ValidationError("some thing went wrong")
    class Meta:
        model = Paper_trading
        fields = ["id","user",'enter_balance']



class PositionSerializer(serializers.ModelSerializer):
    def validate(self,data):
        coin1 = data['coin1']
        coin2 = data['coin2']

        if  Coinlist.check(coin1) and Coinlist.check(coin2):
            return data
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1==coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
        else:
            raise serializers.ValidationError("coin1 and coin2 not found")

    class Meta:
        model = Position
        fields = "__all__"


class PositionCloseSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='c')

    def validate(self,data):
        data.update({'status':'c'})
        view = self.context.get('view')
        id = view.kwargs['pk']
        position = Position.objects.get(id=id)
        WalletManagment.check(position.coin2, position.amount, position.paper_trading)
        return data

    class Meta:
        model = Position
        fields = ['status',]


class PositionAddSerializer(serializers.ModelSerializer):
    paper_trading = serializers.ReadOnlyField(source='paper_trading.id')
    status = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')

    def validate(self,data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        if  Coinlist.check(coin1) and Coinlist.check(coin2):
            user_id = self.context['request'].user.id
            paper_trading = Paper_trading.objects.get(user__id=user_id)
            if data['order_type'] =="l":
                data.update({'status':'w'})
                if data['trade_type'] == "b":
                    is_valid = ValidateWalletCoin.check(data['coin2'], data['amount'], user_id)
                    if is_valid== True :
                        WalletManagment.check(coin2, data['amount']*-1, paper_trading)
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)

                elif data['trade_type'] == "s":
                    is_valid = ValidateWalletCoin.check(data['coin1'], data['amount'], user_id)
                    if is_valid == True :
                        WalletManagment.check(coin1, data['amount']*-1, paper_trading)
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)

            elif data['order_type'] == "m":
                price = PriceChecker.check_price(coin1, coin2)

                if data['trade_type'] == "b":
                    is_valid = ValidateWalletCoin.check(data['coin2'], data['amount'], user_id)
                    if is_valid== True :
                        coin_amount = data['amount'] / PriceChecker.check_price(coin1, coin2)
                        WalletManagment.check(coin2, data['amount']*-1, paper_trading)
                        WalletManagment.check(coin1, coin_amount, paper_trading)
                        data.update({'status':'d'})
                        data.update({'entert_price':price})
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)

                elif data['trade_type'] == "s":
                    coin_amount = data['amount'] * price
                    is_valid = ValidateWalletCoin.check(data['coin1'], data['amount'], user_id)
                    if is_valid == True :
                        WalletManagment.check(coin1, data['amount']*-1, paper_trading)
                        WalletManagment.check(coin2, coin_amount, paper_trading)
                        data.update({'status':'d'})
                        data.update({'entert_price':price})
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)
            return data

        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")

        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")

        elif coin1==coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")

        else:
            raise serializers.ValidationError("coin1 and coin2 not found")

    class Meta:
        model = Position
        fields = "__all__"


class PositionOptionUpdateSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')

    def validate(self,data):
        user = self.context['request'].user
        new_amount = data['amount']
        view = self.context.get('view')
        id = view.kwargs['in_position']
        position = Position.objects.get(id=id)
        position_option = Position_option.objects.get(in_position=position)

        if not position_option.status == "w" and not position_option.trade_type == "w" or not position_option.status == "p" and not position_option.status == "w":
            raise serializers.ValidationError("this position reached or closed !")
        else:
            wallet = Wallet.objects.get(paper_trading__user=user,coin=position.coin1)
            position_amount = position.amount / position.entert_price
            if position_amount>=data['amount'] :
                wallet_result=WalletManagment.check(position.coin1, position_option.amount - new_amount, wallet.paper_trading)
                if wallet_result == True:
                    return data
                else:
                    raise serializers.ValidationError(wallet_result)
            else:
                raise serializers.ValidationError("not enough coin")

    class Meta:
        model = Position_option
        fields ="__all__"


class PositionOptionCreateSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')

    def validate(self,data):
        user = self.context['request'].user
        view = self.context.get('view')
        id = view.kwargs['pk']
        position = Position.objects.get(id=id)
        position_amount = position.amount / position.entert_price
        if position.order_type == "m":
            wallet = Wallet.objects.get(paper_trading__user=user,coin=position.coin1)
            if position_amount>=data['amount'] :
                wallet_result=WalletManagment.check(position.coin1, data['amount'] * -1, wallet.paper_trading)
                if wallet_result == True:
                    if not data['stoploss'] and not data['take_profit']:
                        raise serializers.ValidationError("one of take_profit or stoploss should be fill !")
                    else:
                        data.update({'status':'p'})
                        return data
                else:
                    raise serializers.ValidationError(wallet_result)
            else:
                raise serializers.ValidationError("not enough coin in this position")
        elif position.order_type == "l":
            if position_amount>=data['amount'] :
                if position.order_type == "l":
                    if not data['stoploss'] and not data['take_profit']:
                        raise serializers.ValidationError("one of take_profit or stoploss should be fill !")
                    else:
                        data.update({'status':'p'})
                        return data
            else:
                raise serializers.ValidationError("not enough coin in this position")

    class Meta:
        model = Position_option
        fields ="__all__"


class WalletSerializer(serializers.ModelSerializer):
    class Meta :
        model =Wallet
        fields = "__all__"


class PositionOptionCloseSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='c')
    trade_type = serializers.ReadOnlyField(source='c')
    def validate(self,data):
        data.update({'status':'c','trade_type':'c'})
        view = self.context.get('view')
        id = view.kwargs['in_position']
        position = Position.objects.get(id=id)
        position_option = Position_option.objects.get(in_position=position)
        # back coin to user wallet after position close
        WalletManagment.check(position.coin1, position_option.amount, position.paper_trading)
        return data

    class Meta:
        model = Position_option
        fields = ['status','trade_type',]


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
        elif coin1==coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
            

        results=WatchList_checker.check(coin1,coin2,user)
        if not results:
            raise serializers.ValidationError("repeative coin")
        return data
    class Meta:
        model = Watch_list
        fields = "__all__"

class CoinListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        coins = [Coin_list(**item) for item in validated_data]
        return Coin_list.objects.bulk_create(coins)

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin_list
        fields = "__all__"
        list_serializer_class = CoinListSerializer

