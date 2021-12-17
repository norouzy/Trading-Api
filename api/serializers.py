from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from extentions.checkCoin import Coinlist
from extentions.addToWallet import WalletManagment
# from extentions.watchList import WatchList_checker
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
        return data
    class Meta:
        model = Position
        fields = ['status',]

class PositionAddSerializer(serializers.ModelSerializer):
    paper_trading = serializers.ReadOnlyField(source='paper_trading.id')
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



class PositionOptionSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')
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
