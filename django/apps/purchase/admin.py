from django.contrib import admin
from apps.purchase.models import *


admin.site.register([PurchaseOrder, PurchaseGoods, PurchaseReturnOrder, PurchaseReturnGoods])
