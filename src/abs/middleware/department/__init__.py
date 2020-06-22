# coding=UTF-8

import time

from infrastructure.utils.cache.local import Local
from infrastructure.utils.common.single import Single
from abs.middleware.department.loader import LoaderHelper
from abs.middleware.department.entity import DepartmentEntity



class DepartmentMiddleware(Single):

    def _int(self, root, department_mapping):
        self._root = root
        self._loading_time = time.time()
        self._department_mapping = department_mapping

    def _loading(self):
        department_mapping = {department.id: DepartmentEntity(department) \
                for department in LoaderHelper.loading()}

        root = None
        for dp_id, entity in department_mapping.items():
            parent_id = entity.model.parent_id
            parent_entity = department_mapping.get(parent_id)
            if parent_entity is not None:
                entity.set_parent(parent_entity)
                parent_entity.add_children(entity)
            else:
                root = entity

        self._int(root, department_mapping)
        return root, department_mapping

    def force_refresh(self):
        self._loading()
        return True

    @property
    def is_refresh(self, seconds = 3 * 60):
        return (time.time() - self._loading_time) > seconds

    @property
    def root(self):
        if not hasattr(self, '_root') or self.is_refresh:
            self._loading()
        return self._root

    @property
    def department_mapping(self):
        if not hasattr(self, '_department_mapping') or self.is_refresh:
            self._loading()
        return self._department_mapping

    def get_all_list(self):
        return [entity.model for entity in self.department_mapping.values()]

    def get_root(self):
        return self.root.model

    def get_self(self, department_id):
        return self.department_mapping.get(department_id).model

    def get_children(self, department_id):
        return [entity.model for entity in \
            self.department_mapping.get(department_id).get_children()]

    def get_children_ids(self, department_id):
        entity = self.department_mapping.get(department_id)
        return [et.model.id for et in entity.get_children()]

    def get_parent(self, department_id):
        parent = self.department_mapping.get(department_id).get_parent()
        return None if parent is None else parent.model

    def get_parents(self, department_id):
        entity = self.department_mapping.get(department_id)
        return [et.model for et in entity.get_parents()]

    def get_all_children(self, department_id):
        entity = self.department_mapping.get(department_id)
        return [et.model for et in entity.get_all_children()]

    def get_all_children_ids(self, department_id):
        entity = self.department_mapping.get(department_id)
        return [et.model.id for et in entity.get_all_children()]

    def get_tree(self, department_id):
        entity = self.department_mapping.get(department_id)
        return entity.get_tree()

    def get_list_byids(self, department_ids):
        department_list = []
        for department_id in department_ids:
            if department_id != "":
                department_list.append(self.department_mapping.get(int(department_id)).model)
        return department_list

department_middleware = DepartmentMiddleware()
