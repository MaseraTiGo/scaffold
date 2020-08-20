# coding=UTF-8
import random

from support.common.generator.field.base import BaseHelper


class BrandEntity(BaseHelper):

    def calc(self, has_none = False):
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

    def calc(self, has_none = False):
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

    def calc(self, has_none = False):
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

    def calc(self, has_none = False):
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


class CrnCompanyEntitry(BaseHelper):
    def calc(self, has_none = False):
        from abs.middleground.business.enterprise.models import Enterprise
        company_qs = Enterprise.search(
            license_number = "91420100MA4KM4XY1Y"
        )
        return company_qs[0]


class CrnStaffEntitry(BaseHelper):
    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.crm.staff.models import Staff
            self._enume = []
            for staff in Staff.query():
                self._enume.append(staff)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)


class CustomerEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.customer.personal.store import Customer
            self._enume = []
            for customer in Customer.query():
                self._enume.append(customer)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class SchoolEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.crm.university.store import School
            self._enume = []
            for school in School.query():
                self._enume.append(school)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class MajorEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.crm.university.store import Major
            self._enume = []
            for major in Major.query():
                self._enume.append(major)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class AgentEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.crm.agent.store import Agent
            self._enume = []
            for agent in Agent.query():
                self._enume.append(agent)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class YearsEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.crm.university.store import Years
            self._enume = []
            for years in Years.query():
                self._enume.append(years)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class RelationsEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.crm.university.store import Relations
            self._enume = []
            for relations in Relations.query():
                self._enume.append(relations)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class GoodsEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.agent.goods.store import Goods
            self._enume = []
            for goods in Goods.query():
                self._enume.append(goods)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class AgentCustomerEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.agent.customer.store import AgentCustomer
            self._enume = []
            for agent_customer in AgentCustomer.query():
                self._enume.append(agent_customer)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)

class AgentCustomerChanceEntity(BaseHelper):

    def calc(self, has_none = False):
        if not hasattr(self, '_enume'):
            from abs.services.agent.customer.store import AgentCustomerSaleChance
            self._enume = []
            for sale_chance in AgentCustomerSaleChance.query():
                self._enume.append(sale_chance)

        select_enum = self._enume.copy()
        if has_none:
            select_enum.append(None)
        return random.choice(select_enum)