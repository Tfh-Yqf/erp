from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.system.models import *
import pendulum


def run(*args):
    number = 2
    username = '管理员'
    password = '123456'
    name = '管理员'
    activation_days = 1000
    expiry_time = pendulum.now().add(days=float(activation_days))

    with transaction.atomic():
        team = Team.objects.create(number=number, expiry_time=expiry_time)
        User.objects.create(team=team, username=username, password=make_password(password),
                            name=name, is_manager=True)
