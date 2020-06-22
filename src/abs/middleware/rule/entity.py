# coding=UTF-8


class RuleEntity(object):

    def __init__(self, key, desc):
        self._key = key
        self._desc = desc
        self._parent_entity = None
        self._api_list = []
        self._children_entitys = []

    @property
    def key(self):
        return self._key

    @property
    def desc(self):
        return self._desc

    @property
    def all_key(self):
        if not hasattr(self, '_all_key'):
            keys = self.get_parents()
            keys.reverse()
            keys.append(self)
            self._all_key = '-'.join(entity.key for entity in keys)
        return self._all_key

    @property
    def is_leaf(self):
        return len(self._children_entitys) == 0

    @property
    def is_root(self):
        return self._parent_entity is None

    def set_parent(self, parent_rule):
        self._parent_entity = parent_rule

    def get_parent(self):
        return self._parent_entity

    def get_parents(self):
        all_parent = []
        cur_dp = self
        while True:
            parent = cur_dp.get_parent()
            if parent is not None:
                all_parent.append(parent)
                cur_dp = parent
            else:
                break
        return all_parent

    def add_apis(self, api, *apis):
        self._api_list.append(api)
        if apis:
            self._api_list.extend(apis)

    def get_apis(self):
        return self._api_list

    def add_children(self, rule, *rules):
        self._children_entitys.append(rule)
        if rules:
            self._children_entitys.extend(rules)

    def get_children(self):
        return self._children_entitys

    def get_all_children(self):
        def _add_children(entity, all_children):
            children = entity.get_children()
            for sub_entity in children:
                all_children.append(sub_entity)
                _add_children(sub_entity, all_children)

        all_children = []
        for sub_entity in self.get_children():
            all_children.append(sub_entity)
            _add_children(sub_entity, all_children)

        return all_children

    def remove(self, rule, *rules):
        for ru in ([rule] + rules):
            self._children_entitys.remove(ru)
