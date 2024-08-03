from django.contrib import admin
from apps.data.models import *


admin.site.register([Warehouse, Client, Supplier, Account, ChargeItem])
