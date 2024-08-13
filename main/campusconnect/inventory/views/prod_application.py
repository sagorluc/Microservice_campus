import os
from zzz_lib.zzz_log import zzz_print
import json
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404

from inventory.models.mprod_prei20 import (
    mprod_prei20,
    mprod_prei20_catlist,
   
)

from inventory.views.shopcart.rw_cart_detailview import (
    cartDetailView_byMode,
    cartDetailViewClass
)


#from resumeweb.product_selection import fetchPrei20Randomly
from systemops.fetch_data import (
    fetch_data_faq,
    fetch_data_ta,
    fetch_data_impfact
)

from inventory.fetch_product_data import (
    get_category,
    get_cat_list,
    get_other_services,
)

from productops.product_selection import generate_product_list
from productops.data_prod_comp_v3 import prod_comp_data_prei20



PATH_PRODUCT_LAYOUT     = "inventory/layout/products/application/"
PATH_ROOT               = os.path.join(settings.BASE_DIR)
PATH_PRODUCT_COMPONENT  = 'resumeweb/templates/resumeweb/components/products/exp180'

PRODUCT_LINE        = 'prei20'
PRODUCT_SLOGAN      = 'add slogan hereidentity'
MODEL_PRODUCT       = mprod_prei20
MODEL_PRODUCT_CAT   = mprod_prei20_catlist


