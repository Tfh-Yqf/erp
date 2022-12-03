from django.contrib import admin
from apps.stock_in.models import *


admin.site.register([StockInOrder, StockInGoods, StockInRecord, StockInRecordGoods])
