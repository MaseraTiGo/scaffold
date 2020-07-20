# coding=UTF-8


from support.common.generator.field.base import BaseHelper


class StaffEntity(BaseHelper):

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


class CustomerEntity(BaseHelper):

    def calc(self):
        if not hasattr(self, '_enume'):
            from model.store.model_customer import Customer
            self._enume = []
            for customer in Customer.query():
                self._enume.append(customer)
        return random.choice(self._enume)
