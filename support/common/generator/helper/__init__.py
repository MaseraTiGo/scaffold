# coding=UTF-8


# middleground service generate
from support.common.generator.helper.middleground.person import PersonGenerator
from support.common.generator.helper.middleground.person.address import AddressGenerator
from support.common.generator.helper.middleground.person.bankcard import BankCardGenerator
from support.common.generator.helper.middleground.person.status import StatusGenerator
from support.common.generator.helper.middleground.person.statistics import StatisticsGenerator
from support.common.generator.helper.middleground.enterprise import EnterpriseGenerator
from support.common.generator.helper.middleground.production.brand import BrandGenerator
from support.common.generator.helper.middleground.production import ProductionGenerator
from support.common.generator.helper.middleground.merchandise import MerchandiseGenerator
from support.common.generator.helper.middleground.merchandise.specification import SpecificationGenerator
from support.common.generator.helper.middleground.permission.platform import PlatformGenerator
from support.common.generator.helper.middleground.permission.authorization import AuthorizationGenerator
from support.common.generator.helper.middleground.permission.rule import RuleGenerator
from support.common.generator.helper.middleground.permission.rulegroup import RuleGroupGenerator
from support.common.generator.helper.middleground.permission.position import PositionGenerator
from support.common.generator.helper.middleground.permission.organization import OrganizationGenerator
from support.common.generator.helper.middleground.permission.personposition import PersonPositionGenerator


# crm service generator
from support.common.generator.helper.business.crm.staff import StaffGenerator
from support.common.generator.helper.business.crm.account import StaffAccountGenerator
from support.common.generator.helper.business.crm.university.school import SchoolGenerator
from support.common.generator.helper.business.crm.university.major import MajorGenerator
from support.common.generator.helper.business.crm.university.relations import RelationsGenerator
from support.common.generator.helper.business.crm.university.years import YearsGenerator
from support.common.generator.helper.business.crm.agent import AgentGenerator
from support.common.generator.helper.business.crm.agent.contacts import ContactsGenerator
from support.common.generator.helper.business.crm.adsense.space import SpaceGenerator
from support.common.generator.helper.business.crm.contract.param import ParamGenerator

# customer service generate
from support.common.generator.helper.business.customer.customer import CustomerGenerator
from support.common.generator.helper.business.customer.account import CustomerAccountGenerator
from support.common.generator.helper.business.customer.finance.balance import CustomerBalanceGenerator

# controller service generator
from support.common.generator.helper.business.controller.staff import ControllerStaffGenerator
from support.common.generator.helper.business.controller.account import ControllerStaffAccountGenerator

# agent service generator
from support.common.generator.helper.business.agent.staff import AgentStaffGenerator
from support.common.generator.helper.business.agent.account import AgentStaffAccountGenerator
from support.common.generator.helper.business.agent.goods import GoodsGenerator
