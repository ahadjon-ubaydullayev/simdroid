from rest_framework import serializers
from register.models import *


class SimOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    simcard = serializers.CharField(source='sim_type')
    present = serializers.CharField(source='gift')


    class Meta:
        model = SimOrder
        fields = ('id', 'full_name', 'address', 'tel_number', 'simcard', 'present', 'id_picture', 'id_picture2')




class ClientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Client
        fields = ('id', 'user_id', 'username', 'first_name')

class SimCardOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SimCardOption
        fields = ('sim_type')

         