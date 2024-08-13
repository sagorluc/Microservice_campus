from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views.shopcart.api_views import(
    BuyerInfoViewset,
    McartViewSet,
    # BuyerInfoViewsetAll,
)

router = DefaultRouter()
# router.register(r'buyerinfoall', BuyerInfoViewsetAll, basename='buyerinfoall')
router.register(r'buyerinfo', BuyerInfoViewset, basename='buyerinfo')
router.register(r'mcart', McartViewSet, basename='mcart')

BUYERINFO_MCART_URLS = [
    path('api/', include(router.urls)),
    # path('', include(router.urls)),
]
