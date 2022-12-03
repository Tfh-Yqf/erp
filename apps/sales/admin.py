from django.contrib import admin
from apps.sales.models import *


admin.site.register([SalesOrder, SalesGoods, SalesReturnOrder, SalesReturnGoods])
