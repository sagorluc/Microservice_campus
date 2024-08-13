from rest_framework import serializers
from inventory.models.buyer_info import BuyerInfoModel
from inventory.models.mcart import mcart

class BuyerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BuyerInfoModel
        fields = '__all__'
        
        
        
class McartSerializer(serializers.ModelSerializer):
    class Meta:
        model  = mcart
        fields = '__all__'
        