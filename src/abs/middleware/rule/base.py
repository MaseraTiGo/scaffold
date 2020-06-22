# coding=UTF-8

from infrastructure.utils.common.single import Single
from abs.middleware.rule.entity import RuleEntity


class BaseRule(Single):

    def _load(self):
        fields = [ key for key, val in self.__class__.__dict__.items()\
                  if isinstance(val, RuleEntity)]
        fields.sort()
        root_entity = None
        for key in fields:
            key_list = key.rsplit('_', 1)
            parent_key = key_list[0] if len(key_list) > 1 else None
            cur_entity = getattr(self, key)
            if parent_key is not None:
                parent = getattr(self, parent_key)
                cur_entity.set_parent(parent)
                parent.add_children(cur_entity)
            else:
                root_entity = cur_entity
        return root_entity

    @property
    def root(self):
        if not hasattr(self, "_root"):
            self._root = self._load()
        return self._root

    @property
    def all_mapping(self):
        if not hasattr(self, "_all_mapping"):
            self._all_mapping = self.get_all_mapping()
        return self._root

    def get_all_mapping(self):
        def _create_mapping(entity, all_key_mapping):
            all_key_mapping[entity.all_key] = entity
            for sub_entity in entity.get_children():
                _create_mapping(sub_entity, all_key_mapping)

        all_key_mapping = {}
        _create_mapping(self.root, all_key_mapping)
        return all_key_mapping
