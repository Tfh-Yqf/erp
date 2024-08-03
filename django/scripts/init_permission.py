from apps.system.models import PermissionGroup, Permission


PERMISSIONS = [
    {
        'name': '首页',
        'permissions': [
            {'name': '销售走势', 'code': 'sales_trend'},
            {'name': '销售前十产品', 'code': 'sales_hot_goods'},
            {'name': '入库任务提醒', 'code': 'stock_in_reminder'},
            {'name': '出库任务提醒', 'code': 'stock_out_reminder'},
            {'name': '库存预警', 'code': 'inventory_warning'},
        ],
    },
    {
        'name': '报表统计',
        'permissions': [
            {'name': '销售报表', 'code': 'sales_report'},
            {'name': '采购报表', 'code': 'purchase_report'},
            {'name': '库存报表', 'code': 'inventory'},
            {'name': '批次报表', 'code': 'batch'},
            {'name': '收支统计', 'code': 'finance_statistic'},
        ],
    },
    {
        'name': '基础数据',
        'permissions': [
            {'name': '客户管理', 'code': 'client'},
            {'name': '供应商管理', 'code': 'supplier'},
            {'name': '仓库管理', 'code': 'warehouse'},
            {'name': '结算账户', 'code': 'account'},
            {'name': '收支项目', 'code': 'charge_item'},
        ],
    },
    {
        'name': '产品管理',
        'permissions': [
            {'name': '产品分类', 'code': 'goods_category'},
            {'name': '产品单位', 'code': 'goods_unit'},
            {'name': '产品信息', 'code': 'goods'},
        ],
    },
    {
        'name': '采购管理',
        'permissions': [
            {'name': '采购开单', 'code': 'purchase_order'},
            {'name': '采购退货', 'code': 'purchase_return_order'},
        ],
    },
    {
        'name': '销售管理',
        'permissions': [
            {'name': '销售开单', 'code': 'sales_order'},
            {'name': '销售退货', 'code': 'sales_return_order'},
        ],
    },
    {
        'name': '生产管理',
        'permissions': [
            {'name': '生产计划', 'code': 'production_order'},
            {'name': '生产记录', 'code': 'production_record'},
        ],
    },
    {
        'name': '库内管理',
        'permissions': [
            {'name': '入库', 'code': 'stock_in'},
            {'name': '出库', 'code': 'stock_out'},
            {'name': '盘点', 'code': 'stock_check'},
            {'name': '调拨', 'code': 'stock_transfer'},
            {'name': '库存流水', 'code': 'inventory_flow'},
        ],
    },
    {
        'name': '财务管理',
        'permissions': [
            {'name': '应付欠款', 'code': 'supplier_arrears'},
            {'name': '付款', 'code': 'payment_order'},
            {'name': '应收欠款', 'code': 'client_arrears'},
            {'name': '收款', 'code': 'collection_order'},
            {'name': '账户转账', 'code': 'account_transfer_record'},
            {'name': '日常收支', 'code': 'charge_order'},
            {'name': '资金流水', 'code': 'finance_flow'},
        ],
    },
]


def run(*args):
    PermissionGroup.objects.all().delete()

    for permission_group_item in PERMISSIONS:
        permission_group = PermissionGroup.objects.create(name=permission_group_item['name'])
        Permission.objects.bulk_create([Permission(group=permission_group, name=item['name'], code=item['code'])
                                        for item in permission_group_item['permissions']])
