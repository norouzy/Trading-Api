from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from extentions.checkCoin import Coinlist
from extentions.addToWallet import WalletManagment
from extentions.validateWallet import ValidateWalletCoin
from extentions.CoinPrice import PriceChecker
# from extentions.watchList import WatchList_checker
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
        
        if 'balance' in key and not 'enter_balance' in key: 
            if data['balance']>=0.0:
                return data
            else:
                raise serializers.ValidationError("enter balance cant be under zero")
        else:
            raise serializers.ValidationError("some thing went wrong")
    class Meta:
        model = Paper_trading
        fields = ["id","user", 'balance']


class PositionSerializer(serializers.ModelSerializer):
    def validate(self,data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        if Coinlist.check(coin1) and Coinlist.check(coin2):
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
        print("###########################")
        print(self.context)
        print("###########################")
        view = self.context.get('view')
        id = view.kwargs['pk']
        position = Position.objects.get(id=id)
        print(position.coin2)
        WalletManagment.check(position.coin2, position.amount, position.paper_trading)
        return data
    class Meta:
        model = Position
        fields = ['status', ]


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


class PositionOptionSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    status = serializers.ReadOnlyField(source='p')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')
    def validate(self,data):
        view = self.context.get('view')
        id = view.kwargs['pk']
        position = Position.objects.get(id=id)
        print(position)
        position_amount = position.amount / position.entert_price
        if position_amount>=data['amount']:
            return data
        else:
            raise serializers.ValidationError("not enough coin")

    class Meta:
        model = Position_option
        fields ="__all__"


class WalletSerializer(serializers.ModelSerializer):
    class Meta :
        model =Wallet
        fields = "__all__"



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


class CoinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch_list
        fields = "__all__"
