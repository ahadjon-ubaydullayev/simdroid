from rest_framework import serializers
from register.models import *


class SimOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    simcard = serializers.CharField(source='sim_type')
    present = serializers.CharField(source='gift')
    # photo_url = serializers.SerializerMethodField()
    
    # def get_photo_url(self, sim_order):
    #     request = self.context.get('request')
    #     print("request: ", request)
    #     photo_url = sim_order.id_picture.url
    #     return request.build_absolute_uri(photo_url)

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

         