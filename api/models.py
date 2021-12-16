from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Paper_trading(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="paper_trading", verbose_name="paper trading", blank=True)
    enter_balance = models.FloatField()
    balance = models.FloatField(blank=True, null=True, default=enter_balance)
    enter_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.balance:
            if self.balance <= 0.0:
                self.balance = 0.0
            else:
                self.balance = self.enter_balance
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Coin_list(models.Model):
    coin = models.CharField(max_length=20)
    def __str__(self):
        return self.coin


class Wallet(models.Model):
    paper_trading = models.OneToOneField(Paper_trading, on_delete=models.CASCADE, related_name="Wallet", verbose_name="wallet")

    def __str__(self):
        return f"{self.paper_trading}"
    # coin = models.ForeignKey(Coin_list, models.CASCADE, related_name="coinName")
    # coin = models.CharField(max_length=20)
    # amount = models.FloatField(verbose_name="coin amount")


class WalletItem(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet_item")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_item")
    coin = models.CharField(max_length=20)
    amount = models.FloatField(max_length=15)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.amount < 0:
            self.amount = 0
        super().save(*args, **kwargs)


class Watch_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", verbose_name="user")
    coin = models.CharField(max_length=20)
    # coin1 = models.CharField(max_length=20)
    # coin2 = models.CharField(max_length=20)


class Position(models.Model):
    TRADE_TYPE_CHOISES = (
        ("b", "Buy"),
        ("s", "Sell"),
    )
    STATUS_CHOICES = (
        ("w", "Working"),
        ("d", "Done"),
        ("c", "close"),
    )

    paper_trading = models.ForeignKey(Paper_trading, on_delete=models.CASCADE, related_name="position",verbose_name="position")
    trade_type = models.CharField(max_length=1, choices=TRADE_TYPE_CHOISES, verbose_name="type")
    # coin1 = models.ForeignKey(Coin_list, models.CASCADE, related_name="coin1")
    # coin2 = models.ForeignKey(Coin_list, models.CASCADE, related_name="coin2")
    coin1 = models.CharField(max_length=20)
    coin2 = models.CharField(max_length=20)
    entert_price = models.FloatField()
    amount = models.FloatField(verbose_name="token amount")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="trade status")
    oreder_set_date = models.DateTimeField(auto_now_add=True)
    oreder_reach_date = models.DateTimeField(blank=True, null=True)


    def position_name(self):
        return str(self.paper_trading) + "/" + str(self.coin1) + str(self.coin2)

    def __str__(self):
        return str(self.paper_trading) + "/" + str(self.coin1) + str(self.coin2)


class Position_option(models.Model):
    TRADE_TYPE_CHOISES = (
        ("t", "Take Profit"),
        ("s", "Stop loss"),
        ("w", "Working"),
    )

    STATUS_CHOICES = (
        ("p", "Pending"),
        ("w", "Working"),
        ("d", "Done"),
        ("c", "close"),
    )

    in_position = models.OneToOneField(Position, on_delete=models.CASCADE, related_name="in_position", verbose_name="in_position")
    amount = models.FloatField(verbose_name="token amount")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="trade status")
    trade_type = models.CharField(max_length=1, choices=TRADE_TYPE_CHOISES, verbose_name="trade type", default="w")
    stoploss = models.FloatField(blank=True, null=True)
    take_profit = models.FloatField(blank=True, null=True)
    oreder_reach_date = models.DateTimeField(null=True, blank=True)


    def position_name(self):
        return str(self.in_position.paper_trading) + "/" + str(self.in_position.coin1) + str(self.in_position.coin2)
