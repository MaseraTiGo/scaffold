# coding=UTF-8

from infrastructure.utils.common.single import Single


class BaseMaker(Single):

    def generate_relate(self):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def generate(self):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def run(self, size = 1):
        _generators = []
        for _ in range(size):
            _generator = self.generate()
            _generators.append(_generator)
        return _generators
