# coding=UTF-8

import random
from support.generator.field.base import BaseHelper


class GenderHelper(BaseHelper):

    def calc(self):
        from model.store.model_user import GenderTypes
        return random.choice(GenderTypes.CHOICES)[0]


class EquipStatusHelper(BaseHelper):

    def calc(self):
        from model.store.model_equipment import StatusType
        return random.choice(StatusType.CHOICES)[0]


class PayTypesHelper(BaseHelper):

    def calc(self):
        from model.store.model_order import PayTypes
        return random.choice(PayTypes.CHOICES)[0]


class StaffHelper(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from model.store.model_user import Staff
            self._enume = []
            for staff in Staff.query().filter(id__gt = 1):
                self._enume.append(staff)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)


class MobilePhoneHelper(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from model.store.model_mobilephone import Mobilephone
            self._enume = [None] if has_none else []
            for staff in Mobilephone.query().filter(id__gt = 1):
                self._enume.append(staff)
        return random.choice(self._enume)


class ProductHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            from model.store.model_product import Product
            self._enume = []
            product_qs = Product.query()
            for product in product_qs:
                self._enume.append(product)
        return random.choice(self._enume)


class ProductModelHelper(BaseHelper):

    def calc(self, product_model = None):
        if not hasattr(self, '_enume'):
            from model.store.model_product import ProductModel
            self._enume = []
            product_model_qs = ProductModel.query()
            for pm in product_model_qs:
                self._enume.append(pm)

        return random.choice(self._enume)


class EquipmentModelHelper(BaseHelper):

    def calc(self, product = None, product_model = None, can_send = False):
        if not hasattr(self, '_enume'):
            from model.store.model_equipment import Equipment
            self._enume = []
            equipment_qs = Equipment.query()
            for equipment in equipment_qs:
                self._enume.append(equipment)

        return random.choice(self._enume)
        select_enum = self._enume.copy()
        if product:
            select_enum = filter(lambda obj: obj.product == product, select_enum)

        if product_model:
            select_enum = filter(lambda obj: obj.product_model == product_model, select_enum)

        if can_send:
            select_enum = filter(lambda obj: obj.customer == None, select_enum)

        return random.choice(select_enum)


class GoodsHelper(BaseHelper):

    def calc(self, shop = None, has_none = False):
        if not hasattr(self, '_enume'):
            from model.store.model_shop import Goods
            self._enume = [None] if has_none else []
            goods_qs = Goods.query()
            for goods in goods_qs:
                self._enume.append(goods)

        select_enum = self._enume.copy()
        if shop:
            select_enum = filter(lambda obj: obj.shop == shop, select_enum)
        return random.choice(select_enum)


class CustomerHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            from model.store.model_customer import Customer
            self._enume = []
            for customer in Customer.query():
                self._enume.append(customer)
        return random.choice(self._enume)


class ShopHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            from model.store.model_shop import Shop
            self._enume = []
            for shop in Shop.query():
                self._enume.append(shop)
        return random.choice(self._enume)


class LogisticsItemHelper(BaseHelper):

    def calc(self, is_send = True):
        if not is_send:
            return None

        if not hasattr(self, '_enume'):
            from model.store.model_logistics import LogisticsItem
            self._enume = []
            for item in LogisticsItem.query():
                self._enume.append(item)

        return random.choice(self._enume)


class RoleHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            from model.store.model_role import Role
            from abs.middleware.role import role_middleware
            self._enume = []
            for role in Role.query().filter(id__gt = 1):
                role.parent = role_middleware.get_parent(role.id)
                self._enume.append(role)
        return random.choice(self._enume)


class DepartmentHelper(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            from model.store.model_department import Department
            from abs.middleware.department import department_middleware
            self._enume = []
            for department in Department.query().filter(id__gt = 1):
                department.parent = department_middleware.get_parent(department.id)
                self._enume.append(department)
        return random.choice(self._enume)
