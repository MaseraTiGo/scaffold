# coding=UTF-8


# middleground service generate
from support.common.generator.helper.middleground.person import PersonGenerator
from support.common.generator.helper.middleground.person.address import AddressGenerator
from support.common.generator.helper.middleground.person.bankcard import BankCardGenerator
from support.common.generator.helper.middleground.person.status import StatusGenerator
from support.common.generator.helper.middleground.person.statistics import StatisticsGenerator


# crm service generator
from support.common.generator.helper.business.crm.enterprise import EnterpriseGenerator
from support.common.generator.helper.business.crm.staff import StaffGenerator
from support.common.generator.helper.business.crm.account import StaffAccountGenerator


# customer service generate
from support.common.generator.helper.business.customer.customer import CustomerGenerator
from support.common.generator.helper.business.customer.account import CustomerAccountGenerator
from support.common.generator.helper.business.customer.finance.balance import CustomerBalanceGenerator
