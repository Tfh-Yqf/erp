from extensions.models import *


class Team(Model):

    number = CharField(max_length=32, verbose_name='编号')
    expiry_time = DateTimeField(verbose_name='到期时间')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user_quantity = IntegerField(default=10, verbose_name='用户数量')
    remark = CharField(max_length=256, blank=True, null=True, verbose_name='备注')
    enable_auto_stock_in = BooleanField(default=False, verbose_name='启用自动入库')
    enable_auto_stock_out = BooleanField(default=False, verbose_name='启用自动出库')


class PermissionGroup(Model):
    """权限分组"""

    name = CharField(max_length=64, verbose_name='分组名称')


class Permission(Model):
    """权限"""

    group = ForeignKey('system.PermissionGroup', on_delete=CASCADE, related_name='permissions', verbose_name='权限分组')
    name = CharField(max_length=64, verbose_name='权限名称')
    code = CharField(max_length=64, verbose_name='权限代码')


class Role(Model):
    """角色"""

    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    permissions = ManyToManyField('system.Permission', blank=True, related_name='roles', verbose_name='权限')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='roles')

    class Meta:
        unique_together = [('name', 'team')]


class User(Model):
    """用户"""

    class Sex(TextChoices):
        """性别"""

        MAN = ('man', '男')
        WOMAN = ('woman', '女')

    username = CharField(max_length=32, verbose_name='用户名')
    password = CharField(max_length=256, verbose_name='密码')
    name = CharField(max_length=64, verbose_name='名称')
    phone = CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    email = CharField(max_length=256, null=True, blank=True, verbose_name='邮箱')
    sex = CharField(max_length=32, choices=Sex.choices, verbose_name='性别')
    roles = ManyToManyField('system.Role', blank=True, related_name='users', verbose_name='角色')
    permissions = JSONField(default=list, verbose_name='权限')
    is_manager = BooleanField(default=False, verbose_name='管理员状态')
    is_active = BooleanField(default=True, verbose_name='激活状态')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='users')

    class Meta:
        unique_together = [('username', 'team'), ('name', 'team')]


__all__ = [
    'Team', 'PermissionGroup', 'Permission', 'Role', 'User',
]
