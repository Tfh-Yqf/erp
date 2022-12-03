from django.contrib import admin
from apps.goods.models import *


admin.site.register([GoodsCategory, GoodsUnit, Goods, GoodsImage, Batch, Inventory])
