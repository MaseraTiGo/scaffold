# coding=UTF-8

import time

from infrastructure.utils.cache.local import Local
from infrastructure.utils.common.single import Single
from abs.middleware.role.loader import LoaderHelper
from abs.middleware.role.entity import RoleEntity


class RoleMiddleware(Single):

    def _init(self, root, role_mapping):
        self._role_mapping = role_mapping
        self._root = root
        self._loading_time = time.time()

    def _loading(self):
        role_mapping = {role.id: RoleEntity(role) \
                for role in LoaderHelper.loading()}

        root = None
        for ro_id, entity in role_mapping.items():
            parent_id = entity.model.parent_id
            parent_entity = role_mapping.get(parent_id)
            if parent_entity is not None:
                entity.set_parent(parent_entity)
                parent_entity.add_children(entity)
            else:
                root = entity

        self._init(root, role_mapping)
        return root, role_mapping

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
    def role_mapping(self):
        if not hasattr(self, '_role_mapping') or self.is_refresh:
            self._loading()
        return self._role_mapping

    def get_all_list(self):
        return [entity.model for entity in self.role_mapping.values()]

    def get_root(self):
        return self.root.model

    def get_self(self, role_id):
        return self.role_mapping.get(role_id).model

    def get_children(self, role_id):
        return [entity.model for entity in \
            self.role_mapping.get(role_id).get_children()]

    def get_children_ids(self, role_id):
        entity = self.role_mapping.get(role_id)
        return [et.model.id for et in entity.get_children()]

    def get_parent(self, role_id):
        parent = self.role_mapping.get(role_id).get_parent()
        return None if parent is None else parent.model

    def get_parents(self, role_id):
        entity = self.role_mapping.get(role_id)
        return [et.model for et in entity.get_parents()]

    def get_all_children(self, role_id):
        entity = self.role_mapping.get(role_id)
        return [et.model for et in entity.get_all_children()]

    def get_all_children_ids(self, role_id):
        entity = self.role_mapping.get(role_id)
        return [et.model.id for et in entity.get_all_children()]

    def get_tree(self, role_id):
        entity = self.role_mapping.get(role_id)
        return entity.get_tree()

    def get_list_byids(self, role_ids):
        role_list = []
        for role_id in role_ids:
            if role_id != "":
                role_list.append(self.role_mapping.get(int(role_id)).model)
        return role_list

role_middleware = RoleMiddleware()
