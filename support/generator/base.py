# coding=UTF-8

from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper


class BaseGenerator(object):

    def __init__(self):
        self._input_generators = set()
        self._output_generators = set()
        self._result = None

    @classmethod
    def get_key(cls):
        return cls.__name__.lower()

    def init(self, obj_info):
        obj_infos = []
        if type(obj_info) == list:
            for obj in obj_info:
                obj_infos.append(DictWrapper(obj))
        else:
            obj_infos.append(DictWrapper(obj_info))
        return obj_infos

    def get_create_list(self):
        raise NotImplementedError("please implement this interface!")

    def create(self, *args, **kwargs):
        raise NotImplementedError("please implement this interface!")

    def delete(self):
        raise NotImplementedError("please implement this interface!")

    def has_result(self):
        return self.get_result() is not None

    def get_result(self):
        return self._result

    def reset_result(self):
        self._result = None

    def add_inputs(self, generator, *generators):
        self._input_generators.add(generator)
        if not generator.has_output(self):
            generator.add_outputs(self)

        for generator in generators:
            self._input_generators.add(generator)
            if not generator.has_output(self):
                generator.add_outputs(self)

    def add_outputs(self, generator, *generators):
        self._output_generators.add(generator)
        if not generator.has_input(self):
            generator.add_inputs(self)

        for generator in generators:
            self._output_generators.add(generator)
            if not generator.has_input(self):
                generator.add_inputs(self)

    def get_all(self):
        def _iter(generator, mapping):
            relate_list = []
            relate_list.extend(list(generator.get_inputs()))
            relate_list.extend(list(generator.get_outputs()))

            if generator.get_key() not in mapping:
                mapping[generator.get_key()] = generator.get_result()

            for relate_generator in relate_list:
                if relate_generator.get_key() not in mapping:
                    _iter(relate_generator, mapping)

        _mapping = {}
        _iter(self, _mapping)
        return _mapping

    def get_input_results(self):
        return {generator.get_key(): generator.get_result() \
                for generator in self.get_inputs()}

    def get_output_results(self):
        return {generator.get_key(): generator.get_result() \
                for generator in self.get_outputs()}

    def get_all_results(self):
        return self.get_all()

    def has_input(self, generator):
        return generator in self._input_generators

    def has_output(self, generator):
        return generator in self._output_generators

    def get_inputs(self):
        return self._input_generators

    def get_outputs(self):
        return self._output_generators

    def repair(self, obj, result_mapping):
        return obj

    def generate_exec(self):
        result = []
        result_mapping = self.get_all_results()
        create_list = self.get_create_list(result_mapping)
        logger.info("System is going to generate {}, the staff totle is {}."\
                    .format(self.get_key(), len(create_list)))

        for create_info in create_list:
            try:
                obj = self.create(create_info, result_mapping)
                if obj:
                    result.append(obj)
                    self.repair(obj, result_mapping)
            except Exception as e:
                print("error --> ", e)
                logger.error(" create error! create_info = {}, error = {}"\
                                .format(create_info, e))

        logger.info("System have finished to generate {} data."\
                    .format(self.get_key()))
        return result

    def generate(self, *args, **kwargs):
        for generator in self.get_inputs():
            if not generator.has_result():
                generator.generate()

        if not self.has_result():
            self._result = self.generate_exec()
            if self._result is None:
                raise Exception("{}_create function is need to return result"\
                                .format(self.__class__.__name__))

        for generator in self.get_outputs():
            if not generator.has_result():
                generator.generate()

        return True

    def clear(self):
        for generator in self.get_outputs():
            if generator.has_result():
                generator.clear()

        if self.has_result():
            self.delete()
            self.reset_result()

        for generator in self.get_inputs():
            if generator.has_result():
                generator.clear()
