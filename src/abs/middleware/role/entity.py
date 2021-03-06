# coding=UTF-8


class RoleEntity(object):
    
    def __init__(self, role):
        self._model = role
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
    
    def set_parent(self, parent_role):
        self._parent_entity = parent_role
    
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
        
    def add_children(self, role, *roles):
        self._children_entitys.append(role)
        if roles:
            self._children_entitys.extend(roles)
            
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
    
    def get_tree(self):
        def _get_child_list(sub_entity, children_list):
            for sub_entity in sub_entity.get_children():
                child_list = {
                    "id": sub_entity.model.id,
                    "name": sub_entity.model.name,
                    "describe": self.model.describe,
                    "status": self.model.status,
                    "update_time": self.model.update_time,
                    "children": []
                    }
                children_list["children"].append(child_list)
            
        parent_list = {
                    "id": self.model.id,
                    "name": self.model.name,
                    "describe": self.model.describe,
                    "status": self.model.status,
                    "update_time": self.model.update_time,
                    "children": []
                    }
        
        for sub_entity in self.get_children():          
            child_list = {
                    "id": sub_entity.model.id,
                    "name": sub_entity.model.name,
                    "describe": self.model.describe,
                    "status": self.model.status,
                    "update_time": self.model.update_time,
                    "children": []
                    }
            parent_list["children"].append(child_list)
            _get_child_list(sub_entity, child_list)
        
        return parent_list
    
    def remove(self, role, *roles):
        for ro in ([role] + roles):
            self._children_entitys.remove(ro)