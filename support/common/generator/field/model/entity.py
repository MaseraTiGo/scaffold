# coding=UTF-8
import random

from support.common.generator.field.base import BaseHelper


class BrandEntity(BaseHelper):

    def calc(self, has_none=False):
        if not hasattr(self, '_enume'):
            from abs.middleground.business.production.store import Brand
            self._enume = []
            for brand in Brand.query():
                self._enume.append(brand)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)


class ProductionEntity(BaseHelper):

    def calc(self, has_none=False):
        if not hasattr(self, '_enume'):
            from abs.middleground.business.production.store import Production
            self._enume = []
            for production in Production.query():
                self._enume.append(production)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)


class MerchandiseEntity(BaseHelper):

    def calc(self, has_none=False):
        if not hasattr(self, '_enume'):
            from abs.middleground.business.merchandise.store import \
                    Merchandise
            self._enume = []
            for merchandise in Merchandise.query():
                self._enume.append(merchandise)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)


class SpecificationEntity(BaseHelper):

    def calc(self, has_none=False):
        if not hasattr(self, '_enume'):
            from abs.middleground.business.merchandise.store import \
                    Specification
            self._enume = []
            for specification in Specification.query():
                self._enume.append(specification)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)


class CustomerEntity(BaseHelper):

    def calc(self, has_none=False):
        if not hasattr(self, '_enume'):
            from abs.services.customer.personal.store import Customer
            self._enume = []
            for customer in Customer.query():
                self._enume.append(customer)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)
