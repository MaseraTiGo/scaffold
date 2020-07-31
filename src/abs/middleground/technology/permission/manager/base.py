# coding=UTF-8

import time
from infrastructure.utils.common.dictwrapper import DictWrapper


class Entity(object):

    def __init__(self, model):
        self._model = model
        self._parent_entity = None
        self._children_entitys = []

    @property
    def model(self):
        return self._model

    @property
    def is_leaf(self):
        return len(self._children_entitys) == 0

    @property
    def is_root(self):
        return self._parent_entity is None

    def set_parent(self, parent_model):
        self._parent_entity = parent_model

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

    def add_children(self, model, *models):
        self._children_entitys.append(model)
        if models:
            self._children_entitys.extend(models)

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

    def get_attr_fiels(self):
        raise NotImplemented("this interface is need to implemented!")

    def get_tree(self):
        def _get_attrs(entity):
            attr_list = self.get_attr_fiels()
            result = {}
            for attr in attr_list:
                if hasattr(entity.model, attr):
                    result.update({
                        attr: getattr(entity.model, attr)
                    })
                else:
                    raise Exception("losed attribute [ {} ]".format(attr))
            return result

        def _get_child_list(parent_entity, parent):
            for sub_entity in parent_entity.get_children():
                child = DictWrapper({
                    'id': sub_entity.model.id
                })
                child.update(_get_attrs(sub_entity))
                child.update({'children': []})
                parent['children'].append(child)
                _get_child_list(sub_entity, child)

        root = DictWrapper({
            'id': self.model.id
        })
        root.update(_get_attrs(self))
        root.update({'children': []})

        for sub_entity in self.get_children():
            child = DictWrapper({
                'id': sub_entity.model.id
            })
            child.update(_get_attrs(sub_entity))
            child.update({'children': []})
            root["children"].append(child)
            _get_child_list(sub_entity, child)

        return [root]

    def remove(self, model, *models):
        for dp in ([model] + models):
            self._children_entitys.remove(dp)


class Helper(object):

    ENTITY_CLASS = None

    def _record(self, root, entity_mapping):
        self._entity_mapping = entity_mapping
        self._root = root
        self.loading_time = time.time()

    def get_entity_list(self):
        raise NotImplemented("this interface is need to implemented!")

    def loading(self):
        entity_mapping = {
            entiry.id: self.ENTITY_CLASS(entiry)
            for entiry in self.get_entity_list()
        }

        root = None
        for ro_id, entity in entity_mapping.items():
            parent_id = entity.model.parent_id
            parent_entity = entity_mapping.get(parent_id)
            if parent_entity is not None:
                entity.set_parent(parent_entity)
                parent_entity.add_children(entity)
            else:
                root = entity

        self._record(root, entity_mapping)
        return root, entity_mapping

    def force_refresh(self):
        self.loading()
        return True

    @property
    def is_refresh(self, seconds=30):
        return (time.time() - self.loading_time) > seconds

    @property
    def root(self):
        if not hasattr(self, '_root') or self.is_refresh:
            self.loading()
        return self._root

    @property
    def entity_mapping(self):
        if not hasattr(self, '_entity_mapping') or self.is_refresh:
            self.loading()
        return self._entity_mapping

    def get_all_list(self):
        return [entity.model for entity in self.entity_mapping.values()]

    def get_root(self):
        return self.root.model

    def get_self(self, entity_id):
        return self.entity_mapping.get(entity_id).model

    def get_children(self, entity_id):
        return [
            entity.model
            for entity in self.entity_mapping.get(entity_id).get_children()
        ]

    def get_children_ids(self, entity_id):
        entity = self.entity_mapping.get(entity_id)
        return [et.model.id for et in entity.get_children()]

    def get_parent(self, entity_id):
        parent = self.entity_mapping.get(entity_id).get_parent()
        return None if parent is None else parent.model

    def get_parents(self, entity_id):
        entity = self.entity_mapping.get(entity_id)
        return [et.model for et in entity.get_parents()]

    def get_all_children(self, entity_id):
        entity = self.entity_mapping.get(entity_id)
        return [et.model for et in entity.get_all_children()]

    def get_all_children_ids(self, entity_id):
        entity = self.entity_mapping.get(entity_id)
        return [et.model.id for et in entity.get_all_children()]

    def get_tree(self, entity_id):
        entity = self.entity_mapping.get(entity_id)
        return entity.get_tree()

    def get_list_byids(self, entity_ids):
        entity_list = []
        for entity_id in entity_ids:
            if entity_id != "":
                entity_list.append(
                    self.entity_mapping.get(int(entity_id)).model
                )
        return entity_list
