from inventory.models.mcart import mcart
from inventory.models.buyer_info import BuyerInfoModel
from inventory.serializers import BuyerInfoSerializer, McartSerializer
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

  
class BuyerInfoViewset(viewsets.ModelViewSet):
    queryset = BuyerInfoModel.objects.all()
    serializer_class = BuyerInfoSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email_address', None)
        if email:
            return self.queryset.filter(email_address=email)
        return self.queryset
    

class McartViewSet(viewsets.ModelViewSet):
    queryset = mcart.objects.all()
    serializer_class = McartSerializer

    def get_queryset(self):
        purchase_ids = self.request.query_params.getlist('purchase_ids', None)
        if purchase_ids:
            return self.queryset.filter(mcompleted_purchase__purchase_id__in=purchase_ids)
        return self.queryset

# class BuyerInfoViewset(ViewSet):
#     queryset = BuyerInfoModel.objects.all()
#     serializer_class = BuyerInfoSerializer
    
#     @action(detail=False, methods=['get'], url_path='purchase-history')
#     def get_purchase_his(self, request):
#         email = request.query_params.get('email', None)
#         if email:
#             buyer_email = BuyerInfoModel.objects.filter(email_address=email)
#             serializer = self.get_serializer(buyer_email, many=True)
#             return Response(serializer.data)
#         return Response({'error':'Email parametters is missing'}, status=status.HTTP_400_BAD_REQUEST)
    
