# coding=UTF-8

from support.generator.helper import *
from support.simulate.data.base import BaseMaker

from support.simulate.tool.template.storage import EquipmentTemplate


class StorageMaker(BaseMaker):

    def generate_relate(self, equipment_generator):
        return equipment_generator

    def generate(self):
        equipment = EquipmentGenerator(EquipmentTemplate().generate())

        equipment_generator = self.generate_relate(equipment)
        equipment_generator.generate()
        return equipment_generator
