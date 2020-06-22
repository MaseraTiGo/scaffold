# coding=UTF-8

import os
import profile

from analysis.utils import FileHelper

"""
    需要工具：Graphviz，gprof2doct.py
"""

ANALYSIS_PATH = os.path.abspath(os.path.dirname(__file__))
GPROF2DOT_TOOL_PATH = os.path.join(ANALYSIS_PATH, "gprof2dot.py")
TEMPORARY_PATH = os.path.join(ANALYSIS_PATH, "data")
RESULT_PATH = os.path.join(ANALYSIS_PATH, "graphic")

"""
http://www.graphviz.org/ 需要下载该工具
"""
def run(statement, file_name, sort = -1, data_path = TEMPORARY_PATH, dest_path = RESULT_PATH):
    FileHelper.mk_dirs([data_path, dest_path]) # 初始化目录

    prof = profile.Profile()
    try:
        prof = prof.run(statement)
    except SystemExit:
        pass

    if file_name is not None:
        data_file_name = "%s.stats" % os.path.join(data_path, file_name)
        prof.dump_stats(data_file_name)
#         flag_1 = os.system(r"python %s -f pstats %s" % (GPROF2DOT_TOOL_PATH, data_file_name))
#         flag_2 = os.system(r"dot -Tpng -o %s.png %s" % (os.path.join(dest_path, file_name), data_file_name))

        flag = os.system(r"python3 %s -f pstats %s | dot -Tpng -o %s.png" % (GPROF2DOT_TOOL_PATH, data_file_name, os.path.join(dest_path, file_name)))
        if flag:
            print("generate png error")

    return prof.print_stats(sort)
