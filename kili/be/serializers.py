from rest_framework import serializers
from django.db.models import Sum

from .models import Client, CurrentAccount, Movement


class ClientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
        )


class CurrentAccountSerializer(serializers.ModelSerializer):

    moves = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = CurrentAccount
        fields = (
            'id',
            'moves',
            'balance'
        )

    def get_moves(self, obj):
        return list(obj.movements.values('id', 'created', 'description', 'amount').order_by('-created'))

    def get_balance(self, obj):
        return obj.movements.aggregate(Sum('amount'))


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = (
            'id',
            'amount',
            'account',
            'description',
            'created'
        )

