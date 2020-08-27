# coding=UTF-8


def gen_meta(name, *classes, **conf):
    return type(name, tuple(classes), conf) 

def with_metaclass(cls, *classes, **conf):
    # return type('tmp' + cls.__name__, (cls, ), {'a':1})()
    e_list = [cls]
    e_list.extend(classes)
    conf.update(cls.__dict__)
    conf.update({'__dict__':cls.__dict__})
    return_obj = gen_meta("tmp"+cls.__name__, *e_list, **conf)
    return return_obj
